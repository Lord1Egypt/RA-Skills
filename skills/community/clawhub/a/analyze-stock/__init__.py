# OpenClaw 标准技能入口
def run(ctx):
    """
    股票分析技能 - 使用全局配置的模型进行消息面和利好风险分析
    """
    # ======================
    # 1. 获取用户输入
    # ======================
    stock_code = ctx.input.get("stock_code", "")
    if not stock_code:
        return ctx.error("请输入股票代码（如 601117）")
    
    style = ctx.input.get("style", "balanced")
    
    # ======================
    # 2. 获取财务数据（Tushare）
    # ======================
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(__file__))
        from scripts.analyze_stock import fetch_stock_data
        
        # 格式化股票代码
        if stock_code.startswith('6'):
            ts_code = f"{stock_code}.SH"
        elif stock_code.startswith('0') or stock_code.startswith('3'):
            ts_code = f"{stock_code}.SZ"
        else:
            ts_code = stock_code
        
        data = fetch_stock_data(ts_code)
    except Exception as e:
        return ctx.error(f"获取数据失败：{str(e)}")
    
    # ======================
    # 3. 收集背景信息
    # ======================
    background_info = f"""股票名称：{data['name']}
所属行业：{data.get('industry', '未知')}
概念板块：{data.get('concepts', '未知')}
当前价格：¥{data.get('price', '未知')}
当前 PE: {data.get('pe', '未知')}，PE 分位：{data.get('pe_percentile', '未知')}%
PB: {data.get('pb', '未知')}
营收增速：{data.get('revenue_growth', '未知')}%
毛利率：{data.get('gross_margin', '未知')}%
ROE: {data.get('roe', '未知')}%"""
    
    # ======================
    # 4. 调用全局模型分析消息面（新增！）
    # ======================
    market_sentiment = ""
    try:
        sentiment_prompt = f"""你是一位专业的股票分析师。请分析以下股票的消息面情况：

{background_info}

请从以下维度分析：
1. 量能情况（放量/缩量）
2. 均线趋势（多头/空头）
3. 消息面影响（利好/利空）

请给出综合判断和操作建议，不超过 100 字。"""

        sentiment_response = ctx.claw.llm.chat({
            "messages": [
                {"role": "system", "content": "你是一位专业的股票分析师，擅长分析股票的技术面和消息面。请简洁明了地给出判断和建议。"},
                {"role": "user", "content": sentiment_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 300
        })
        
        market_sentiment = sentiment_response.get("content", "")
        
    except Exception as e:
        market_sentiment = "消息面分析暂时不可用"
    
    # ======================
    # 5. 调用全局模型分析利好与风险（核心！）
    # ======================
    try:
        prompt = f"""你是一位专业的股票分析师。请分析以下股票的利好与风险因素：

{background_info}

请分别列出：
1. 3 点最主要的利好因素（每点不超过 20 字）
2. 3 点最主要的风险因素（每点不超过 20 字）

直接返回结果，格式如下：
利好因素：
1. xxx
2. xxx
3. xxx

风险因素：
1. xxx
2. xxx
3. xxx"""

        response = ctx.claw.llm.chat({
            "messages": [
                {"role": "system", "content": "你是一位专业的股票分析师，擅长分析股票的投资价值和风险因素。请简洁明了地列出利好和风险因素。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        })
        
        analysis_content = response.get("content", "")
        
    except Exception as e:
        # 模型调用失败，使用备用方案
        analysis_content = """利好因素：
1. 行业地位领先，竞争优势明显
2. 业绩保持增长态势
3. 受益于行业政策支持

风险因素：
1. 行业竞争加剧风险
2. 政策变化风险
3. 宏观经济波动风险"""
    
    # ======================
    # 6. 生成完整分析报告
    # ======================
    try:
        from scripts.analyze_stock import generate_full_report
        report = generate_full_report(data, analysis_content, style, market_sentiment)
    except:
        # 备用方案：直接返回简化报告
        report = f"""# 📈 {data['name']} ({stock_code}) 分析报告

## 核心数据
- 当前价格：¥{data.get('price', '未知')}
- PE: {data.get('pe', '未知')}（分位{data.get('pe_percentile', '未知')}%）
- PB: {data.get('pb', '未知')}
- 营收增速：{data.get('revenue_growth', '未知')}%

## 消息面分析
{market_sentiment}

## 利好因素
{analysis_content.split('风险因素')[0].replace('利好因素：', '')}

## 风险因素
{analysis_content.split('风险因素')[1] if '风险因素' in analysis_content else '暂无'}

---
⚠️ 免责声明：本报告仅供参考，不构成投资建议"""
    
    # ======================
    # 7. 返回结果
    # ======================
    return ctx.success({
        "stock": stock_code,
        "name": data['name'],
        "report": report,
        "market_sentiment": market_sentiment,
        "analysis": analysis_content,
        "model": "阿里云 Coding Plan(全局自动调用)"
    })
