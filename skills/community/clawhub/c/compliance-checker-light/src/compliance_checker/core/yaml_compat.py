"""
YAML 兼容层

提供 YAML 解析功能，当 PyYAML 不可用时使用简单实现。
这是一个工具函数模块，保留具体实现。
"""


def simple_yaml_load(text: str) -> dict:
    """
    简单的 YAML 解析器，支持基本结构：
    - 键值对
    - 嵌套对象
    - 列表（包括对象列表）
    - 基本类型（字符串、数字、布尔值）
    """
    lines = text.split("\n")

    def parse_value(val: str):
        """解析单个值"""
        val = val.strip()

        if val == "" or val == "null" or val == "~":
            return None

        # 布尔值
        if val in ["true", "True", "TRUE", "yes", "Yes", "YES"]:
            return True
        if val in ["false", "False", "FALSE", "no", "No", "NO"]:
            return False

        # 字符串引号
        if (val.startswith('"') and val.endswith('"')) or (
            val.startswith("'") and val.endswith("'")
        ):
            return val[1:-1]

        # 内联列表 [a, b, c]
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1]
            if not inner.strip():
                return []
            items = []
            # 处理带引号的字符串
            current = ""
            in_quote = False
            quote_char = None
            for char in inner:
                if char in "\"'":
                    if not in_quote:
                        in_quote = True
                        quote_char = char
                    elif char == quote_char:
                        in_quote = False
                        quote_char = None
                    else:
                        current += char
                elif char == "," and not in_quote:
                    items.append(parse_value(current.strip()))
                    current = ""
                else:
                    current += char
            if current.strip():
                items.append(parse_value(current.strip()))
            return items

        # 数字
        try:
            if "." in val:
                return float(val)
            return int(val)
        except ValueError:
            pass

        # 字符串
        return val

    def get_indent(line: str) -> int:
        return len(line) - len(line.lstrip())

    def parse_block(lines: list, start_idx: int, base_indent: int) -> tuple:
        """
        解析一个代码块（对象或列表）
        返回 (result, next_idx)
        """
        result = {}
        i = start_idx
        current_list = None
        current_list_key = None

        while i < len(lines):
            line = lines[i]

            # 跳过空行和注释
            if not line.strip() or line.strip().startswith("#"):
                i += 1
                continue

            indent = get_indent(line)

            # 如果缩进小于基线，说明块结束了
            if indent < base_indent:
                break

            content = line.strip()

            # 处理列表项
            if content.startswith("- "):
                # 如果当前在构建对象，切换到列表模式
                if current_list is None:
                    current_list = []
                    if current_list_key:
                        result[current_list_key] = current_list

                item_content = content[2:].strip()

                # 检查是否有嵌套属性
                next_idx = i + 1
                while next_idx < len(lines) and (
                    not lines[next_idx].strip() or lines[next_idx].strip().startswith("#")
                ):
                    next_idx += 1

                has_nested = False
                if next_idx < len(lines):
                    next_indent = get_indent(lines[next_idx])
                    next_content = lines[next_idx].strip()
                    if next_indent > indent and not next_content.startswith("- "):
                        has_nested = True

                if has_nested or (
                    ":" in item_content
                    and parse_value(item_content.split(":", 1)[1].strip()) is None
                ):
                    # 对象列表项
                    if ":" in item_content:
                        key, val = item_content.split(":", 1)
                        key = key.strip()
                        val = val.strip()
                        if val == "":
                            # 嵌套对象
                            nested_obj, i = parse_block(lines, next_idx, next_indent)
                            nested_obj[key] = nested_obj.pop(key, {})
                            # 重新组织
                            new_obj = {key: nested_obj.get(key, {})}
                            for k, v in nested_obj.items():
                                if k != key:
                                    new_obj[k] = v
                            current_list.append(new_obj)
                        else:
                            obj = {key: parse_value(val)}
                            # 检查是否有更多属性
                            while next_idx < len(lines):
                                next_line = lines[next_idx]
                                if not next_line.strip() or next_line.strip().startswith("#"):
                                    next_idx += 1
                                    continue
                                next_indent = get_indent(next_line)
                                if next_indent <= indent:
                                    break
                                if next_line.strip().startswith("- "):
                                    break
                                # 解析嵌套属性
                                nested_obj, consumed = parse_block(lines, next_idx, next_indent)
                                obj.update(nested_obj)
                                next_idx = consumed
                            current_list.append(obj)
                            i = next_idx
                            continue
                    else:
                        # 纯列表项，但有嵌套
                        nested_obj, i = parse_block(lines, next_idx, next_indent)
                        current_list.append(nested_obj)
                        continue
                else:
                    # 简单列表项
                    if ":" in item_content:
                        key, val = item_content.split(":", 1)
                        current_list.append({key.strip(): parse_value(val.strip())})
                    else:
                        current_list.append(parse_value(item_content))

            # 处理键值对
            elif ":" in content:
                key, val = content.split(":", 1)
                key = key.strip()
                val = val.strip()

                if val == "":
                    # 可能是嵌套对象或列表
                    next_idx = i + 1
                    while next_idx < len(lines) and (
                        not lines[next_idx].strip() or lines[next_idx].strip().startswith("#")
                    ):
                        next_idx += 1

                    if next_idx >= len(lines):
                        result[key] = None
                    else:
                        next_indent = get_indent(lines[next_idx])
                        next_content = lines[next_idx].strip()

                        if next_content.startswith("- "):
                            # 列表开始
                            current_list = []
                            result[key] = current_list
                            current_list_key = key
                            i = next_idx
                            continue
                        else:
                            # 嵌套对象
                            nested_obj, i = parse_block(lines, next_idx, next_indent)
                            result[key] = nested_obj
                            continue
                else:
                    result[key] = parse_value(val)

            i += 1

        return result, i

    result, _ = parse_block(lines, 0, 0)
    return result


# 尝试导入 PyYAML，失败则使用简单实现
try:
    import yaml

    safe_load = yaml.safe_load
except ImportError:
    safe_load = simple_yaml_load
