#!/usr/bin/env python3
"""L2 — Schema/Data Quality Checker: JSON Schema validation, data integrity, format compliance"""

import json, sys, os, re, time
from typing import Optional

# ── Built-in test schemas ──
SCHEMA_TEST_CASES = {
    "contact": {
        "schema": {
            "type": "object",
            "properties": {
                "name": {"type":"string","minLength":1},
                "phone": {"type":"string","pattern":"^1[3-9]\\d{9}$"},
                "email": {"type":"string","format":"email"},
                "age": {"type":"integer","minimum":0,"maximum":150}
            },
            "required": ["name","phone"]
        },
        "pass_cases": [
            {"name":"张三","phone":"13800138000","email":"zhangsan@test.com","age":28},
            {"name":"李四","phone":"15912345678","email":"lisi@test.com","age":35},
        ],
        "fail_cases": [
            {"name":"","phone":"12345"},                          # empty name + bad phone
            {"name":"王五","phone":"110"},                         # bad phone format
            {"name":"赵六","phone":"13800138000","age":200},       # age out of range
            {},                                                     # missing required fields
        ]
    },
    "flight_booking": {
        "schema": {
            "type": "object",
            "properties": {
                "flight_no": {"type":"string","pattern":"^[A-Z]{2}\\d{3,4}$"},
                "date": {"type":"string","pattern":"^\\d{4}-\\d{2}-\\d{2}$"},
                "passengers": {"type":"array","items":{"type":"object",
                    "properties":{"name":{"type":"string"},"id_card":{"type":"string","pattern":"^\\d{18}$"}},
                    "required":["name"]},"minItems":1},
                "class": {"type":"string","enum":["economy","business","first"]}
            },
            "required": ["flight_no","date","passengers"]
        },
        "pass_cases": [
            {"flight_no":"CA1234","date":"2026-08-15",
             "passengers":[{"name":"张三","id_card":"110101199001011234"}],"class":"economy"},
        ],
        "fail_cases": [
            {"flight_no":"123","date":"2026/08/15","passengers":[],"class":"gold"},
            {"flight_no":"MU00001","date":"2026-13-01","passengers":[{"name":"李四","id_card":"123"}],"class":"economy"},
        ]
    },
    "ai_response": {
        "schema": {
            "type": "object",
            "properties": {
                "content": {"type":"string","minLength":1},
                "confidence": {"type":"number","minimum":0,"maximum":1},
                "source": {"type":"array","items":{"type":"string"}},
                "metadata": {"type":"object","properties":{"model":{"type":"string"},"latency_ms":{"type":"integer"}}}
            },
            "required": ["content"]
        },
        "pass_cases": [
            {"content":"北京是中国的首都","confidence":0.95,"source":["wiki"],"metadata":{"model":"gpt-4","latency":320}},
        ],
        "fail_cases": [
            {},                                             # missing content
            {"content":"","confidence":99},                 # empty content, confidence > 1
        ]
    }
}

class SchemaChecker:
    def __init__(self):
        self.results = []

    def validate(self, instance: dict, schema: dict, name: str = "unnamed") -> dict:
        """Validate a single instance against JSON Schema (draft-07 subset)"""
        errors = []
        t0 = time.time()

        # Type check
        SCHEMA_TYPE_MAP = {"object":dict,"string":str,"integer":int,"number":(int,float),"array":list,"boolean":bool}
        expected_type = schema.get("type")
        expected_py_type = SCHEMA_TYPE_MAP.get(expected_type)
        if expected_py_type and not isinstance(instance, expected_py_type):
            errors.append(f"类型错误: 期望{expected_type}, 实际{type(instance).__name__}")

        if expected_type == "object":
            props = schema.get("properties",{})
            required = schema.get("required",[])

            # Required fields
            for req in required:
                if req not in instance:
                    errors.append(f"缺少必填字段: {req}")

            # Per-field checks
            for field, value in instance.items():
                if field not in props:
                    continue
                ps = props[field]
                ft = ps.get("type")

                # Type
                TYPE_MAP = {"string":str,"integer":int,"number":(int,float),"array":list,"object":dict,"boolean":bool}
                expected_py_type = TYPE_MAP.get(ft)
                if expected_py_type and not isinstance(value, expected_py_type):
                    errors.append(f"字段[{field}]类型错误: 期望{ft}, 实际{type(value).__name__}")
                    continue

                # String validations
                if ft == "string":
                    if ps.get("minLength",0) > 0 and len(value) < ps["minLength"]:
                        errors.append(f"字段[{field}]过短({len(value)}<{ps['minLength']})")
                    if ps.get("maxLength") and len(value) > ps["maxLength"]:
                        errors.append(f"字段[{field}]过长({len(value)}>{ps['maxLength']})")
                    pattern = ps.get("pattern")
                    if pattern and not re.match(pattern, str(value)):
                        errors.append(f"字段[{field}]格式不匹配: {value}")

                # Integer validations
                if ft == "integer":
                    if ps.get("minimum") is not None and value < ps["minimum"]:
                        errors.append(f"字段[{field}]小于最小值({value}<{ps['minimum']})")
                    if ps.get("maximum") is not None and value > ps["maximum"]:
                        errors.append(f"字段[{field}]大于最大值({value}>{ps['maximum']})")

                # Number validations
                if ft == "number":
                    if ps.get("minimum") is not None and value < ps["minimum"]:
                        errors.append(f"字段[{field}]小于最小值")
                    if ps.get("maximum") is not None and value > ps["maximum"]:
                        errors.append(f"字段[{field}]大于最大值")

                # Array validations
                if ft == "array":
                    if ps.get("minItems") and len(value) < ps["minItems"]:
                        errors.append(f"字段[{field}]数组过少({len(value)}<{ps['minItems']})")
                    item_schema = ps.get("items",{})
                    for i, item in enumerate(value):
                        sub = self.validate(item, item_schema, f"{name}[{field}][{i}]")
                        errors.extend(sub.get("errors",[]))

                # Enum check
                enum_vals = ps.get("enum")
                if enum_vals and value not in enum_vals:
                    errors.append(f"字段[{field}]不在枚举中: {value} ∉ {enum_vals}")

        elapsed = round(time.time()-t0, 4)
        return {"name": name, "valid": len(errors)==0, "errors": errors, "latency": elapsed}

    def run_all(self) -> dict:
        results = []
        stats = {"schemas": 0, "pass_cases": 0, "fail_cases": 0,
                 "expected_pass": 0, "expected_fail": 0,
                 "tp": 0, "fp": 0, "tn": 0, "fn": 0}

        for schema_name, test_data in SCHEMA_TEST_CASES.items():
            schema = test_data["schema"]
            stats["schemas"] += 1

            # Test pass cases (should validate)
            for instance in test_data["pass_cases"]:
                r = self.validate(instance, schema, f"{schema_name}/pass")
                stats["pass_cases"] += 1
                stats["expected_pass"] += 1
                if r["valid"]: stats["tp"] += 1
                else: stats["fn"] += 1
                results.append(r)

            # Test fail cases (should reject)
            for instance in test_data["fail_cases"]:
                r = self.validate(instance, schema, f"{schema_name}/fail")
                stats["fail_cases"] += 1
                stats["expected_fail"] += 1
                if not r["valid"]: stats["tn"] += 1
                else: stats["fp"] += 1
                results.append(r)

        stats["total"] = stats["pass_cases"] + stats["fail_cases"]
        stats["sensitivity"] = round(stats["tp"]/(stats["tp"]+stats["fn"])*100,1) if (stats["tp"]+stats["fn"])>0 else 0
        stats["specificity"] = round(stats["tn"]/(stats["tn"]+stats["fp"])*100,1) if (stats["tn"]+stats["fp"])>0 else 0
        stats["accuracy"] = round((stats["tp"]+stats["tn"])/stats["total"]*100,1) if stats["total"]>0 else 0

        self.results = results
        return stats

    def validate_file(self, filepath: str, schema: dict) -> list:
        """Validate all JSON objects in a file"""
        results = []
        with open(filepath,"r") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line: continue
                try:
                    instance = json.loads(line)
                    r = self.validate(instance, schema, f"{filepath}:{i}")
                    results.append(r)
                except json.JSONDecodeError as e:
                    results.append({"name":f"{filepath}:{i}","valid":False,"errors":[f"JSON解析错误: {e}"],"latency":0})
        return results

def generate_report(stats: dict, path: Optional[str] = None) -> str:
    lines = [f"# Schema 合规性检查报告\n"]
    lines.append(f"Schema总量: {stats['schemas']} | 用例总量: {stats['total']}\n")
    lines.append(f"## 指标\n")
    lines.append(f"- 准确率 (Accuracy): {stats['accuracy']}%")
    lines.append(f"- 敏感度 (Sensitivity/Recall): {stats['sensitivity']}%")
    lines.append(f"- 特异度 (Specificity): {stats['specificity']}%")
    lines.append(f"- TP={stats['tp']} TN={stats['tn']} FP={stats['fp']} FN={stats['fn']}\n")
    report = "\n".join(lines)
    if path: open(path,"w").write(report)
    return report

if __name__ == "__main__":
    checker = SchemaChecker()
    stats = checker.run_all()
    print(generate_report(stats))
    # Print details
    for r in checker.results:
        status = "✅" if r["valid"] else "❌"
        errs = "; ".join(r["errors"]) if r["errors"] else ""
        print(f"  {status} {r['name']}: {errs[:80]}")
    sys.exit(0 if stats["accuracy"]==100 else 1)
