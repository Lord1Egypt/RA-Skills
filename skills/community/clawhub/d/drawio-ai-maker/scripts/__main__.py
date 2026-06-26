#!/usr/bin/env python3
"""
__main__.py - drawio-generator 技能主入口

支持两种运行模式：
1. 分析模式（默认）：接收原始描述 → 返回 LLM prompt
   → 供主 agent 调用 MiniMax，分析后把 JSON 结果回传

2. 生成模式（--from-llm）：接收 JSON 结果 → 生成 XML → 校验 → 成功则交付 / 失败则打回

用法：
  # 分析模式：需要主 agent 调用 MiniMax
  python3 __main__.py --title "用户登录" --input "描述文字"

  # 生成模式：主 agent 注入了 LLM 分析结果（带校验）
  python3 __main__.py --title "用户登录" --from-llm '{"title":"...","nodes":[...],"edges":[...]}'
"""
import argparse
import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path

# 添加 agent_harness 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from designer import generate_structured_description
from generator import generate_drawio_xml
from validator import validate_drawio_xml, validate_json_schema

OUTPUT_DIR = Path(os.environ.get("DRAWIO_OUTPUT_DIR", "/Users/owen/Desktop/drawio-generator"))
MAX_RETRIES = 3  # 最多打回重写次数


def main():
    parser = argparse.ArgumentParser(description='drawio-generator: 文字描述 → draw.io 图表')
    parser.add_argument('--title', type=str, default=None, help='图表标题')
    parser.add_argument('--input', type=str, default=None, help='原始描述文字（分析模式）')
    parser.add_argument('--from-llm', type=str, default=None,
                        help='JSON 结果（生成模式，主 agent 注入了 LLM 分析结果）')
    parser.add_argument('--type', type=str, default=None,
                        help='图表类型提示: flowchart|sequence|network|architecture|hierarchy|function|deployment')
    parser.add_argument('--output-dir', type=str, default=str(OUTPUT_DIR),
                        help=f'输出目录 (默认: {OUTPUT_DIR})')
    parser.add_argument('--retry', type=int, default=0,
                        help='当前重试次数（内部使用）')

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    # 生成模式：主 agent 已注入 LLM 结果
    if args.from_llm:
        result_json = _parse_llm_result(args.from_llm)
        _run_generation_with_validation(result_json, args.output_dir, args.retry)
        return

    # 分析模式：需要 LLM 分析
    if args.input:
        _run_analysis(args.input, args.title, args.type, args.output_dir)
        return

    # 交互模式：从 stdin 读取
    print("=" * 60, flush=True)
    print("Step 1: 接收输入", flush=True)
    print("=" * 60, flush=True)
    print("请输入图表描述文字（输入空行结束）：", flush=True)

    lines = []
    while True:
        try:
            line = input()
            if line.strip() == '':
                break
            lines.append(line)
        except EOFError:
            break

    if not lines:
        print("未输入描述，退出。", flush=True)
        sys.exit(0)

    text = '\n'.join(lines)
    print(f"✓ 已读取文字 ({len(text)} 字符)", flush=True)
    _run_analysis(text, args.title, args.type, args.output_dir)


def _parse_llm_result(llm_output: str) -> dict:
    """解析 LLM 输出（可能是纯 JSON 或带前后缀的文本）"""
    stripped = llm_output.strip()
    if stripped.startswith('{') and stripped.endswith('}'):
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            pass

    match = re.search(r'\{[\s\S]*\}', stripped)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM 结果无法解析为 JSON: {e}\n内容: {stripped[:500]}")

    raise ValueError(f"LLM 结果中未找到 JSON: {stripped[:200]}")


def _run_analysis(text: str, title: str, chart_type: str, output_dir: str):
    """分析模式：构建 prompt，打印指令给主 agent"""
    # 检测是否已经是 JSON
    if text.strip().startswith('{') and '"title"' in text:
        try:
            result = json.loads(text)
            _run_generation_with_validation(result, output_dir, 0)
            return
        except json.JSONDecodeError:
            pass

    print("=" * 60, flush=True)
    print("Step 2: LLM 分析 → 结构化设计描述", flush=True)
    print("=" * 60, flush=True)

    design = generate_structured_description(text, chart_type)

    if not design.get('needs_llm', True):
        print(f"✓ 使用内置规则生成设计（简单描述）", flush=True)
        _run_generation_with_validation(design['result'], output_dir, 0)
        return

    llm_prompt = design['llm_prompt']

    print("\n" + "=" * 60, flush=True)
    print("⚠️ 需要 LLM 分析 — 请将以下内容发送给主 agent", flush=True)
    print("=" * 60, flush=True)

    instruction = {
        'action': 'llm_analysis',
        'prompt': llm_prompt,
        'hint': f'请用 MiniMax 分析以下 prompt，返回纯 JSON 结果（不带任何前缀说明）：\n\n{llm_prompt}',
        'output_format': '--from-llm \'{{"title":"...","nodes":[...],"edges":[...]}}\'',
        'example': '--from-llm \'{"title":"用户登录流程","type":"flowchart","nodes":[{"id":"0","label":"开始","type":"start","x":200,"y":50,"width":120,"height":60}],"edges":[]}\''
    }

    print(json.dumps(instruction, ensure_ascii=False, indent=2), flush=True)

    print("\n" + "=" * 60, flush=True)
    print("📋 主 agent 应执行：", flush=True)
    print("=" * 60, flush=True)
    print(f"1. 调用 MiniMax LLM，分析 prompt\n", flush=True)
    print("2. 把 JSON 结果通过以下命令回传：", flush=True)
    print(f"   python3 __main__.py --from-llm '<JSON结果>'", flush=True)
    print()


def _run_generation_with_validation(structured: dict, output_dir: str, retry_count: int):
    """
    生成模式（带校验 + 打回机制）：
    JSON → XML → 校验 → 成功交付 / 失败打回 LLM
    """
    title = structured.get('title', '未命名图表')
    date_str = datetime.now().strftime('%Y%m%d')
    safe_title = ''.join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
    filename = f"{safe_title}_{date_str}"
    drawio_path = Path(output_dir) / f"{filename}.drawio"

    # 阶段1: JSON Schema 校验
    print("=" * 60, flush=True)
    print(f"Step A: JSON Schema 校验 (第 {retry_count + 1} 次尝试)", flush=True)
    print("=" * 60, flush=True)

    json_valid = validate_json_schema(structured)
    if not json_valid['valid']:
        print(f"❌ JSON Schema 校验失败:", flush=True)
        for err in json_valid['errors']:
            print(f"   - {err}", flush=True)
        _emit_retry_instruction(structured, json_valid['errors'], "JSON Schema 校验失败")
        sys.exit(1)

    print(f"✓ JSON Schema 校验通过", flush=True)

    # 阶段2: 生成 XML
    print("=" * 60, flush=True)
    print("Step B: 生成 draw.io XML", flush=True)
    print("=" * 60, flush=True)

    try:
        xml_content = generate_drawio_xml(structured)
        print(f"✓ XML 生成成功 ({len(xml_content)} 字节)", flush=True)
    except Exception as e:
        print(f"❌ XML 生成异常: {e}", flush=True)
        _emit_retry_instruction(structured, [str(e)], "XML 生成异常")
        sys.exit(1)

    # 阶段3: 规则校验
    print("=" * 60, flush=True)
    print("Step C: XML 规则校验", flush=True)
    print("=" * 60, flush=True)

    validation = validate_drawio_xml(xml_content)
    if not validation['valid']:
        print(f"❌ XML 校验失败，共 {len(validation['errors'])} 个错误:", flush=True)
        for err in validation['errors']:
            print(f"   - {err}", flush=True)

        if retry_count >= MAX_RETRIES:
            print(f"\n⚠️ 已达到最大重试次数 ({MAX_RETRIES})，放弃生成", flush=True)
            print("错误汇总:", json.dumps(validation['errors'], ensure_ascii=False), flush=True)
            sys.exit(1)

        _emit_retry_instruction(structured, validation['errors'], "XML 校验失败")
        sys.exit(1)

    print(f"✓ XML 校验通过", flush=True)
    stats = validation['stats']
    print(f"   节点数: {stats['vertices']}, 边数: {stats['edges']}", flush=True)
    print(f"   vertex IDs: {stats['vertex_ids']}", flush=True)
    print(f"   edge IDs: {stats['edge_ids']}", flush=True)

    # 阶段4: 保存文件
    print("=" * 60, flush=True)
    print("Step D: 保存文件", flush=True)
    print("=" * 60, flush=True)

    with open(drawio_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"✓ 已保存: {drawio_path}", flush=True)

    # 最终交付
    print("\n" + "=" * 60, flush=True)
    print("✅ 图表生成完毕（校验通过）", flush=True)
    print("=" * 60, flush=True)
    print(f".drawio: {drawio_path}", flush=True)


def _emit_retry_instruction(structured: dict, errors: list, reason: str):
    """
    打印打回指令，告诉主 agent 如何让 LLM 重新生成。
    """
    print("\n" + "=" * 60, flush=True)
    print(f"🔄 打回 LLM 重新生成 — {reason}", flush=True)
    print("=" * 60, flush=True)

    # 构建详细的修正 prompt
    correction_prompt = f"""上一次生成失败，原因如下：
{chr(10).join(f"- {e}" for e in errors)}

请修正以下 JSON描述，重新生成符合规范的 draw.io XML 数据：

原始 JSON：
{json.dumps(structured, ensure_ascii=False, indent=2)}

**必须满足的 XML 规则：**
1. vertex id 从 10 开始（如 10,11,12...）
2. edge id 从 20 开始（如 20,21,22...）
3. 每个 vertex 必须有 parent="1"，每个 edge 必须有 parent="0"
4. edge 的 source/target 必须引用存在的 vertex id
5. nodes 必须包含 x, y, width, height（自动布局不可靠，必须手动计算坐标）
6. edges 必须包含 id, source, target
7. 水平间距 ≥ 180px，垂直间距 ≥ 140px
8. 形状规则：
   - 起始/结束：ellipse，宽120 高50
   - 判断：rhombus，宽190 高70（Y下N右）
   - 处理步骤：rounded=1，按文字长度算宽高
9. 箭头样式：endArrow=classic（单向箭头，不要 orthogonalEdgeStyle）
10. 分支布局：判断的N(否)分支放到右侧，Y(是)分支向下

**坐标计算参考（画布宽850，主轴居中x=425）：**
- 主轴节点：x = 425 - width/2
- 右侧分支：x = 650 或更大
- 垂直间距：上一节点 y + 上一节点 height + 140px

请返回修正后的纯 JSON，不要包含任何说明文字。
"""

    print("📋 修正指令（让 LLM 重新生成）:", flush=True)
    print(correction_prompt, flush=True)

    retry_cmd = (
        f'python3 __main__.py --from-llm \''
        f'{json.dumps(structured, ensure_ascii=False)}'
        f'\' --retry 1'
    ).replace("'", "'\"'\"'")

    print(f"\n📌 快速重试命令:", flush=True)
    print(f"   {retry_cmd}", flush=True)


if __name__ == '__main__':
    main()
