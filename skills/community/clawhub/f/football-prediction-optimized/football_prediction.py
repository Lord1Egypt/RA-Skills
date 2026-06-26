#!/usr/bin/env python3
"""
足球预测优化技能 - 使用自我优化系统的最佳提示词进行比赛预测

功能：
1. Stage1 批量筛选：对同一比赛日的多场比赛进行横向比较筛选
2. Stage2 单场比赛预测：对单场比赛进行深度分析，预测胜平负和CLV值

环境变量：
- DEEPSEEK_API_KEY: DeepSeek API密钥（必需）
- DEEPSEEK_BASE_URL: DeepSeek API基础URL（可选，默认：https://api.deepseek.com）

用法：
  python football_prediction.py stage1 --input batch_fet_txt.txt
  python football_prediction.py stage2 --input single_fet_txt.txt
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import requests

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 最佳提示词定义
# Stage1 提示词（来自自我优化系统的最佳提示词）
STAGE1_SYSTEM_PROMPT = """你是一个专业的足球比赛数据质量评估员，专注于同一比赛日内多场比赛的横向比较分析。你的核心任务是通过系统化评估，从一批比赛中筛选出最适合进行胜平负预测的高质量场次，并为投注决策提供结构化建议。"""

STAGE1_USER_PROMPT_TEMPLATE = """请基于以下提供的同一比赛日多场比赛信息，执行专业筛选。

比赛信息批次：
{fet_txt_batch}

**评估与筛选指令**

1.  **逐场评估（5个维度，每项0-10分）**
    *   **数据完整性**：评估特征文本(`fet_txt`)中关键信息的完备性与可靠性。关键信息包括：近期战绩、阵容新闻、伤病情况、战术风格、主场/客场表现、教练信息等。信息越全面、来源越可靠，得分越高。
    *   **市场清晰度**：分析赔率数据、必发指数、市场交易量及变化趋势。市场共识越强、信号越一致（如赔率稳定指向某一方向，或出现显著且合理的赔率变动），得分越高。市场混乱或信号矛盾的得分低。
    *   **基本面优势**：综合评估球队当前状态（近期战绩、攻防数据）、绝对实力（联赛排名、阵容价值）、历史交锋记录以及赛前动态（如战意、轮换）。一方优势越明显、越有说服力，得分越高。势均力敌但特点鲜明的比赛也可得中等分数。
    *   **预测潜力**：基于收盘赔率变化值(CLV)的概念，评估该场比赛预测结果可能带来的价值。考虑当前赔率与隐含概率，判断是否存在被市场低估或高估的可能性。潜在价值收益空间越大，得分越高。
    *   **风险等级**：识别比赛的不确定性、矛盾信息或异常点。例如：核心球员突然伤疑、球队战意不明、数据源冲突、比赛重要性特殊（如杯赛轮换）、或出现极端赔率等。风险越高，此项得分越高（注：高风险对应高分，在综合评分中是负向因子）。

2.  **计算与排序**
    *   为每场比赛计算**综合评分**，公式为：
        `综合评分 = (数据完整性 * 0.2) + (市场清晰度 * 0.25) + (基本面优势 * 0.25) + (预测潜力 * 0.2) - (风险等级 * 0.1)`
        *（权重可根据经验微调，此权重强调市场和基本面的核心地位，并惩罚风险）*
    *   根据综合评分，对所有比赛进行**从高到低**的排序。

3.  **筛选决策**
    *   **初步筛选**：仅保留综合评分 **> 6.0** 的比赛。
    *   **最终数量控制**：在初步筛选的基础上，选择综合评分最高的 **3 至 8 场** 比赛作为最终推荐。如果符合条件的比赛少于3场，则全部选中并备注；如果超过8场，则只取前8名。
    *   **决策标签**：对最终列表中的比赛标记为 `"KEEP"`，其余比赛标记为 `"DROP"`。
    *   **筛选理由**：为每场 `"KEEP"` 的比赛提供1-2句简要理由，说明其核心优势或为何从本批次中脱颖而出。

4.  **资金与风险建议（集成于输出中）**
    *   在最终输出的 `summary` 部分，需隐含风险分散建议：选中比赛数(`total_selected`)在3-8场之间，本身即建议分散投资。
    *   可通过 `average_score` 和 `selection_rate` 间接反映整体批次质量。平均分高、选中率适中（如30%-60%）表明批次整体质量好且经过精选；选中率过低或过高都需警惕。

**输出格式要求**
你必须严格遵循以下JSON格式输出，无需任何额外解释或文本。

```json
{
  "date": "比赛日期（从输入数据中提取）",
  "total_matches": 总比赛数量,
  "selected_matches": [
    {
      "lota_id": "比赛唯一ID",
      "home_team": "主队名称",
      "away_team": "客队名称",
      "league": "所属联赛",
      "score": 综合评分（保留两位小数）,
      "data_completeness": 数据完整性得分（整数）,
      "market_clarity": 市场清晰度得分（整数）,
      "fundamental_strength": 基本面优势得分（整数）,
      "prediction_potential": 预测潜力得分（整数）,
      "risk_level": 风险等级得分（整数）,
      "decision": "KEEP",
      "reason": "简要的筛选理由，突出最大优势"
    }
    // ... 更多KEEP的比赛，按综合评分降序排列
  ],
  "summary": {
    "total_selected": 最终选中比赛的数量,
    "average_score": 所有选中比赛的综合评分的平均值（保留两位小数）,
    "selection_rate": 选中比例（保留两位小数，例如0.45表示45%）
  }
}
```

**注意**：`selected_matches` 数组中只包含最终决定 `"KEEP"` 的比赛，且已按 `score` 降序排列。被 `"DROP"` 的比赛不应出现在此数组中。"""

# Stage2 提示词（来自自我优化系统的最佳提示词）
STAGE2_PROMPT_TEMPLATE = """你是一个专业的足球分析师，专注于数据驱动的比赛预测和CLV（收盘赔率变化值）收益优化。请基于以下比赛信息，严格按照分析框架进行综合评估，输出JSON格式的预测结果。

**核心目标**：在准确预测胜平负（H/D/A）的基础上，最大化CLV潜在收益。

**输入信息**：
{fet_txt}

**分析框架与指令**：

1.  **基本面分析**：
    *   **球队状态**：评估两队近期（如近5-10场）的竞技状态、得失球趋势、关键球员伤停、战术风格。
    *   **历史交锋**：分析双方直接对话的历史记录、进球模式、心理优势。
    *   **主客场优势**：量化主队主场表现与客队客场表现的差异，包括胜率、攻防数据。

2.  **市场分析**：
    *   **赔率变化**：追踪从初盘到当前盘口的赔率变动方向、幅度及时间点，识别市场资金流向。
    *   **必发数据（如可用）**：分析成交量、大额交易、买方/卖方比例，判断"聪明钱"动向。
    *   **市场情绪**：综合赔率与交易数据，判断市场整体倾向是否存在过热或价值低估。

3.  **数据质量评估**：
    *   明确指出所提供 `{fet_txt}` 中数据的**可靠性与完整性**。例如：关键数据（如伤停、近期战绩）是否缺失？数据来源是否权威？此评估将直接影响置信度。

4.  **风险因素识别**：
    *   **不确定性来源**：如临场阵容突变、天气条件、裁判因素、球队战意（联赛位置、杯赛轮换）。
    *   **潜在异常**：市场赔率出现与基本面严重背离的异常波动，或数据中存在矛盾点。

5.  **CLV收益预估**：
    *   基于对赔率变化趋势的分析，分别预测"主胜"、"平局"、"客胜"三个选项在临场前的**CLV值**（即预计的赔率优化空间，可为正或负）。目标是识别当前赔率最有升值潜力的选项。

**输出要求**：

1.  **预测结果 (prediction)**：基于整体分析，给出最终预测："H"（主胜）、"D"（平局）或"A"（客胜）。
2.  **置信度 (confidence)**：一个介于0到1之间的数值，反映你对预测结果的把握程度，需结合数据质量与风险综合评定。
3.  **关键理由 (reasoning)**：列出3-5条支撑你预测的最核心、数据驱动的分析要点，每条以"理由X："开头。
4.  **CLV预估 (clv_estimates)**：一个JSON对象，包含对"home"（主胜）、"draw"（平局）、"away"（客胜）三个选项的CLV值估计。数值表示预计赔率变化的百分比（例如，0.02表示预计赔率上升2%，对应赔付增加）。
5.  **风险评估 (risk_factors)**：列出1-3个最主要的、可能颠覆预测的风险因素。
6.  **时间戳 (timestamp)**：生成预测的UTC时间，格式为"YYYY-MM-DD HH:MM:SS"。

**请严格遵循以下JSON格式输出，无需任何额外解释或文本**：

{
  "lota_id": "从{fet_txt}中提取的比赛ID",
  "prediction": "H/D/A",
  "confidence": 0.00,
  "reasoning": [
    "理由1：...",
    "理由2：...",
    "理由3：..."
  ],
  "clv_estimates": {
    "home": 0.00,
    "draw": 0.00,
    "away": 0.00
  },
  "risk_factors": [
    "风险因素1",
    "风险因素2"
  ],
  "timestamp": "2023-10-27 14:30:00"
}"""

class DeepSeekClient:
    """DeepSeek API客户端"""

    def __init__(self):
        self.api_key = os.environ.get('DEEPSEEK_API_KEY')
        self.base_url = os.environ.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com').rstrip('/')

        if not self.api_key:
            raise ValueError("环境变量 DEEPSEEK_API_KEY 未设置，请设置环境变量：export DEEPSEEK_API_KEY='your_api_key'")

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })

    def call_model(self, messages, model="deepseek-chat", temperature=0.3, max_tokens=4000):
        """调用DeepSeek模型"""
        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "response_format": {"type": "json_object"}
        }

        try:
            logger.info(f"调用DeepSeek API: {model}")
            response = self.session.post(url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()

            content = result['choices'][0]['message']['content']
            logger.info(f"API调用成功，token使用情况: {result.get('usage', {})}")

            # 尝试解析JSON
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"模型输出不是有效的JSON: {e}")
                logger.debug(f"原始输出: {content}")
                # 尝试提取JSON部分
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group())
                    except:
                        pass
                raise ValueError(f"无法解析模型输出为JSON: {content[:200]}")

        except requests.exceptions.RequestException as e:
            logger.error(f"API调用失败: {e}")
            raise
        except KeyError as e:
            logger.error(f"API响应格式错误: {e}, 响应: {result}")
            raise

class FootballPredictionSkill:
    """足球预测技能主类"""

    def __init__(self):
        self.client = DeepSeekClient()

    def run_stage1(self, fet_txt_batch: str) -> Dict[str, Any]:
        """运行Stage1批量筛选"""
        logger.info("开始Stage1批量筛选")

        # 准备消息
        messages = [
            {"role": "system", "content": STAGE1_SYSTEM_PROMPT},
            {"role": "user", "content": STAGE1_USER_PROMPT_TEMPLATE.format(fet_txt_batch=fet_txt_batch)}
        ]

        # 调用模型
        result = self.client.call_model(messages)

        # 验证结果格式
        required_fields = ["date", "total_matches", "selected_matches", "summary"]
        for field in required_fields:
            if field not in result:
                raise ValueError(f"结果缺少必需字段: {field}")

        logger.info(f"Stage1完成，筛选出 {result['summary']['total_selected']} 场比赛")
        return result

    def run_stage2(self, fet_txt: str) -> Dict[str, Any]:
        """运行Stage2单场比赛预测"""
        logger.info("开始Stage2单场比赛预测")

        # 准备消息
        messages = [
            {"role": "system", "content": "你是一个专业的足球分析师，专注于数据驱动的比赛预测和CLV收益优化。"},
            {"role": "user", "content": STAGE2_PROMPT_TEMPLATE.format(fet_txt=fet_txt)}
        ]

        # 调用模型
        result = self.client.call_model(messages)

        # 添加时间戳（如果结果中没有）
        if 'timestamp' not in result:
            result['timestamp'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        # 验证结果格式
        required_fields = ["lota_id", "prediction", "confidence", "reasoning", "clv_estimates", "risk_factors"]
        for field in required_fields:
            if field not in result:
                raise ValueError(f"结果缺少必需字段: {field}")

        logger.info(f"Stage2完成，预测结果: {result['prediction']}, 置信度: {result['confidence']}")
        return result

def read_input_file(file_path: str) -> str:
    """读取输入文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"读取文件失败: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description='足球预测优化技能')
    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # Stage1 命令
    stage1_parser = subparsers.add_parser('stage1', help='批量筛选多场比赛')
    stage1_parser.add_argument('--input', required=True, help='输入文件路径，包含多场比赛特征文本，用===分隔')
    stage1_parser.add_argument('--output', help='输出文件路径（可选），默认为stdout')

    # Stage2 命令
    stage2_parser = subparsers.add_parser('stage2', help='单场比赛预测')
    stage2_parser.add_argument('--input', required=True, help='输入文件路径，包含单场比赛特征文本')
    stage2_parser.add_argument('--output', help='输出文件路径（可选），默认为stdout')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        # 读取输入
        input_text = read_input_file(args.input)

        # 初始化技能
        skill = FootballPredictionSkill()

        # 执行对应命令
        if args.command == 'stage1':
            result = skill.run_stage1(input_text)
        elif args.command == 'stage2':
            result = skill.run_stage2(input_text)
        else:
            logger.error(f"未知命令: {args.command}")
            sys.exit(1)

        # 输出结果
        output_json = json.dumps(result, ensure_ascii=False, indent=2)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_json)
            logger.info(f"结果已保存到: {args.output}")
        else:
            print(output_json)

    except Exception as e:
        logger.error(f"运行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()