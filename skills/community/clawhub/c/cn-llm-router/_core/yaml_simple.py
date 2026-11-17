"""极简 YAML 解析器（自研，零依赖）。

仅支持本技能 models.yaml 用到的子集：
- 映射（嵌套，2 空格缩进）
- 序列（`- ` 列表，元素可为标量或嵌套映射）
- 标量：字符串 / 整数 / 浮点 / 布尔 / null
- `#` 注释

不追求完整 YAML 规范，只为「模型注册表」这一个可控文件服务。
如环境已装 PyYAML 可走更完整解析；这里保证零依赖也能跑。
"""

import sys


def _scalar(s):
    s = s.strip()
    if s == "" or s in ("null", "~", "None"):
        return None
    if s in ("true", "True"):
        return True
    if s in ("false", "False"):
        return False
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def _preprocess(text):
    out = []
    for raw in text.split("\n"):
        line = raw.rstrip("\r")
        if not line.strip():
            continue
        if line.lstrip().startswith("#"):
            continue
        # 去掉行尾注释（仅在空白后出现的 #）
        hp = line.find(" #")
        if hp != -1:
            line = line[:hp]
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        out.append((indent, line.strip()))
    return out


def load(text):
    lines = _preprocess(text)
    pos = [0]

    def parse_block(indent):
        if pos[0] >= len(lines):
            return None
        ind, content = lines[pos[0]]
        if content == "-" or content.startswith("- "):
            return parse_seq(indent)
        return parse_map(indent)

    def parse_map(indent):
        result = {}
        while pos[0] < len(lines):
            ind, content = lines[pos[0]]
            if ind < indent:
                break
            if ind > indent:
                pos[0] += 1
                continue
            if content == "-" or content.startswith("- "):
                break
            if ":" not in content:
                pos[0] += 1
                continue
            k, _, v = content.partition(":")
            k = k.strip()
            v = v.strip()
            pos[0] += 1
            if v == "":
                if pos[0] < len(lines):
                    nind, _ = lines[pos[0]]
                    if nind > indent:
                        result[k] = parse_block(nind)
                    else:
                        result[k] = None
                else:
                    result[k] = None
            else:
                result[k] = _scalar(v)
        return result

    def parse_seq(indent):
        items = []
        while pos[0] < len(lines):
            ind, content = lines[pos[0]]
            if ind < indent or (content != "-" and not content.startswith("- ")):
                break
            rest = content[1:].strip()
            pos[0] += 1
            if rest == "":
                if pos[0] < len(lines):
                    nind, _ = lines[pos[0]]
                    if nind > indent:
                        items.append(parse_block(nind))
                    else:
                        items.append(None)
                else:
                    items.append(None)
            else:
                items.append(_scalar(rest))
        return items

    return parse_block(0)


def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return load(f.read())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        import json
        print(json.dumps(load_file(sys.argv[1]), ensure_ascii=False, indent=2))


# ───────────────────────── 极简 YAML 写入器 ─────────────────────────
def _yaml_scalar(v):
    """把 Python 标量转为 YAML 标量文本。"""
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, int) or isinstance(v, float):
        return str(v)
    # 字符串：含特殊字符时加引号
    s = str(v)
    if any(c in s for c in ":{}[]&*?|-><!%@`") or s.startswith(("'", '"')):
        return '"' + s.replace('"', '\\"') + '"'
    return s


def _dump_mapping(mapping, indent_level=0):
    """把 dict 序列化为 YAML 映射文本。"""
    lines = []
    prefix = "  " * indent_level
    for k, v in mapping.items():
        if isinstance(v, dict):
            lines.append(prefix + str(k) + ":")
            lines.append(_dump_mapping(v, indent_level + 1))
        elif isinstance(v, list):
            lines.append(prefix + str(k) + ":")
            lines.append(_dump_seq(v, indent_level + 1))
        else:
            lines.append(prefix + str(k) + ": " + _yaml_scalar(v))
    return "\n".join(lines)


def _dump_seq(seq, indent_level=0):
    """把 list 序列化为 YAML 序列文本。"""
    lines = []
    prefix = "  " * indent_level
    for item in seq:
        if isinstance(item, dict):
            # 序列中的映射：第一项前加 "- "，后续行缩进
            first = True
            for k, v in item.items():
                if isinstance(v, (dict, list)):
                    if first:
                        lines.append(prefix + "- " + str(k) + ":")
                        first = False
                    else:
                        lines.append(prefix + "  " + str(k) + ":")
                    if isinstance(v, dict):
                        lines.append(_dump_mapping(v, indent_level + 1))
                    else:
                        lines.append(_dump_seq(v, indent_level + 1))
                else:
                    if first:
                        lines.append(prefix + "- " + str(k) + ": " + _yaml_scalar(v))
                        first = False
                    else:
                        lines.append(prefix + "  " + str(k) + ": " + _yaml_scalar(v))
        else:
            lines.append(prefix + "- " + _yaml_scalar(item))
    return "\n".join(lines)


def dump(data):
    """把 Python 对象序列化为 YAML 文本（顶层为映射）。"""
    if not isinstance(data, dict):
        raise ValueError("顶层必须是映射")
    return _dump_mapping(data)


def dump_file(path, data):
    """把 Python 对象写入 YAML 文件。"""
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(dump(data))

