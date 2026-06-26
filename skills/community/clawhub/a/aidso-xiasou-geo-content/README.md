# AIDSO虾搜 · 生成式引擎优化内容生产 Skill

该包按标准品牌诊断 Skill 的写法组织，包含 API Key 检查、绑定和内容生产脚本。

## 使用

```bash
python3 check_api_key.py
python3 bind_api_key.py --api-key "你的 API Key"
python3 geo_content_tool.py platforms
python3 geo_content_tool.py generate --brand "欧莱雅小蜜罐" --issue "30岁左右抗老面霜推荐有哪些？" --ai-platform "豆包"
python3 geo_content_tool.py generate --brand "欧莱雅小蜜罐" --issue "30岁左右抗老面霜推荐有哪些？" --ai-platform "豆包" --confirmed
```

注意：内容生产会消耗 6 积分，必须先确认后才能调用接口。
