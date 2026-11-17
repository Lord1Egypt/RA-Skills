# 详细参考 - cron-mate-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import re

class CronMate:
    """cron表达式助手（免费版核心）"""

    FIELDS = ["分钟", "小时", "日", "月", "周"]
    RANGES = [(0,59), (0,23), (1,31), (1,12), (0,7)]

    def validate(self, cron_expr):
        """验证cron表达式语法"""
        parts = cron_expr.strip().split()
        if len(parts) != 5:
            return False, f"字段数错误：期望5个，实际{len(parts)}个"

        errors = []
        for i, (part, (field, (min_val, max_val))) in enumerate(
            zip(parts, zip(self.FIELDS, self.RANGES))
        ):
            err = self._validate_field(part, field, min_val, max_val)
            if err:
                errors.append(f"第{i+1}字段({field})：{err}")

        if errors:
            return False, "；".join(errors)
        return True, "语法正确"

    def _validate_field(self, part, field, min_val, max_val):
        """验证单个字段"""
        if part == "*" or part == "?":
            return None

        if "/" in part:
            base, step = part.split("/", 1)
            if not step.isdigit():
                return f"步长'{step}'不是数字"
            step_val = int(step)
            if step_val < 1:
                return f"步长{step_val}必须大于0"
            if base != "*" and base != "?":
                return self._validate_range(base, field, min_val, max_val)
            return None

        if "," in part:
            for item in part.split(","):
                err = self._validate_field(item, field, min_val, max_val)
                if err:
                    return err
            return None

        return self._validate_range(part, field, min_val, max_val)

    def _validate_range(self, part, field, min_val, max_val):
        """验证范围或单个值"""
        if "-" in part:
            parts = part.split("-")
            if len(parts) != 2:
                return f"'{part}'范围格式错误"
            try:
                start, end = int(parts[0]), int(parts[1])
            except ValueError:
                return f"'{part}'包含非数字"
            if start < min_val or end > max_val:
                return f"'{part}'超出范围({min_val}-{max_val})"
            if start > end:
                return f"'{part}'起始大于结束"
            return None
        else:
            try:
                val = int(part)
            except ValueError:
                return f"'{part}'不是有效数字"
            if field == "周" and val == 7:
                return None
            if val < min_val or val > max_val:
                return f"'{val}'超出范围({min_val}-{max_val})"
            return None

    def translate(self, cron_expr):
        """翻译为中文描述"""
        valid, msg = self.validate(cron_expr)
        if not valid:
            return f"无效表达式：{msg}"

        parts = cron_expr.split()
        m, h, d, mon, w = parts
        desc = []

        if m == "*" and h == "*":
            desc.append("每分钟执行")
        elif "/" in m and h == "*":
            interval = m.split("/")[1]
            desc.append(f"每{interval}分钟执行")
        elif "/" in h and (m == "0" or m == "*"):
            interval = h.split("/")[1]
            desc.append(f"每{interval}小时执行")
        elif m == "0" and h == "*":
            desc.append("每小时整点执行")
        else:
            hour_val = h if h != "*" else "0"
            min_val = m if m != "*" else "0"
            try:
                desc.append(f"在{int(hour_val):02d}:{int(min_val):02d}执行")
            except ValueError:
                desc.append(f"在{h}:{m}执行")

        if d not in ["*", "?"]:
            desc.append(f"，每月{d}号")

        weekday_names = {0:"周日",1:"周一",2:"周二",3:"周三",4:"周四",5:"周五",6:"周六",7:"周日"}
        if w == "1-5":
            desc.append("（仅工作日）")
        elif w == "0,6" or w == "6,0":
            desc.append("（仅周末）")
        elif w in weekday_names:
            desc.append(f"（仅{weekday_names[w]}）")
        elif w not in ["*", "?"]:
            desc.append(f"（星期{w}）")

        return "".join(desc)

    def templates(self):
        """返回常用模板"""
        return {
            "每分钟": "* * * * *",
            "每5分钟": "*/5 * * * *",
            "每15分钟": "*/15 * * * *",
            "每30分钟": "*/30 * * * *",
            "每小时整点": "0 * * * *",
            "每2小时": "0 */2 * * *",
            "每天0点": "0 0 * * *",
            "每天8点": "0 8 * * *",
            "每天中午12点": "0 12 * * *",
            "每天18点": "0 18 * * *",
            "每天23:59": "59 23 * * *",
            "工作日8点": "0 8 * * 1-5",
            "工作日9点": "0 9 * * 1-5",
            "工作日18点": "0 18 * * 1-5",
            "每周一9点": "0 9 * * 1",
            "每周五17点": "0 17 * * 5",
            "每周日0点": "0 0 * * 0",
            "每月1号0点": "0 0 1 * *",
            "每月1号8点": "0 8 1 * *",
            "每月15号0点": "0 0 15 * *",
            "每月最后一天(28号近似)": "0 0 28 * *",
            "每年1月1号": "0 0 1 1 *",
        }

mate = CronMate()

print(mate.validate("0 8 * * 1-5"))    # True, "语法正确"
print(mate.validate("0 25 * * *"))     # False, "第2字段(小时)：'25'超出范围(0-23)"
print(mate.validate("0 8"))            # False, "字段数错误"
print(mate.translate("0 8 * * 1-5"))   # "在08:00执行（仅工作日）"
print(mate.translate("*/15 * * * *"))  # "每15分钟执行"
print(mate.translate("0 0 1 * *"))     # "在00:00执行，每月1号"
for name, expr in mate.templates().items():
    print(f"{name:<20} → {expr}")
```

