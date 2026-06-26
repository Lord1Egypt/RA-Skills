# CNC Quote Skill - 安装使用指南

## 安装方式

### 方式一: ClawHub 一键安装 (推荐)

```bash
openclaw skill install cnc-quote-skill
```

### 方式二: 从源码安装

```bash
git clone https://github.com/openclaw-community/cnc-quote-skill.git
cd cnc-quote-skill
openclaw skill install .
```

### 方式三: 手动复制

```bash
# 复制到 OpenClaw skills 目录
cp -r cnc-quote-skill ~/.openclaw/skills/
```

## 配置

### 1. 设置 API 密钥

```bash
# 编辑配置文件
nano ~/.openclaw/config.json

# 添加 DashScope API
{
  "channels": {
    "dashscope": {
      "apiKey": "YOUR_API_KEY_HERE"
    }
  }
}
```

### 2. 初始化数据库

```python
from cnc_quote_skill import QuoteEngine

# 首次运行会自动创建数据库
engine = QuoteEngine()
```

### 3. 导入训练数据

```bash
# 如果有历史报价数据
python -m cnc_quote_skill.import_data --file your_quotes.json
```

## 验证安装

```python
from cnc_quote_skill import QuoteEngine

engine = QuoteEngine()
result = engine.calculate({
    "material": "AL6061",
    "dimensions": {"length": 100, "width": 50, "height": 20},
    "surface_treatment": "anodizing",
    "quantity": 100
})

print(f"✅ 安装成功! 报价结果: ¥{result.total_price}")
```

## 集成到现有系统

### QQ Bot 集成

```python
# 在你的 QQ Bot 处理器中
from cnc_quote_skill import QuoteEngine

engine = QuoteEngine()

async def handle_quote_request(message):
    # 解析用户输入
    order = parse_order(message)
    # 计算报价
    result = engine.calculate(order)
    # 返回结果
    return format_response(result)
```

### API 服务

```python
from flask import Flask, request, jsonify
from cnc_quote_skill import QuoteEngine

app = Flask(__name__)
engine = QuoteEngine()

@app.route('/api/quote', methods=['POST'])
def quote():
    order = request.json
    result = engine.calculate(order)
    return jsonify({
        "price": result.total_price,
        "confidence": result.confidence,
        "risks": result.risk_flags
    })

if __name__ == '__main__':
    app.run(port=5000)
```

## 常见问题

### Q: 准确率不够高怎么办?

A: 添加更多训练数据。准确率与数据量正相关:
- 100 条数据: ~80% 准确率
- 500 条数据: ~90% 准确率
- 1000+ 条数据: ~94% 准确率

### Q: 如何添加新材料?

A: 编辑 `config/material_pricing.json`:

```json
{
  "新材料名称": {
    "density": 2.7,
    "price_per_kg": 50,
    "machinability": 0.8
  }
}
```

### Q: 如何调整风险敏感度?

A: 编辑 `config/quote_settings.json`:

```json
{
  "risk_sensitivity": "high",  // low, medium, high
  "confidence_threshold": 0.7  // 0.5 - 0.9
}
```

## 更新

```bash
# 更新到最新版本
openclaw skill update cnc-quote-skill
```

## 卸载

```bash
openclaw skill uninstall cnc-quote-skill
```