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
