# 抖音爆款标题生成器测试脚本

Write-Host "🧪 开始测试抖音爆款标题生成器..." -ForegroundColor Cyan

# 测试1：基础功能
Write-Host "`n📋 测试1：基础标题生成" -ForegroundColor Yellow
python main.py --topic "美食制作" --style "搞笑" --count 2

# 测试2：多种风格
Write-Host "`n📋 测试2：多种风格生成" -ForegroundColor Yellow
python main.py --topic "健身减脂" --style "励志" --count 2

# 测试3：结合热点
Write-Host "`n📋 测试3：结合热点话题" -ForegroundColor Yellow
python main.py --topic "美食制作" --trending "减肥" --count 2

# 测试4：指定受众
Write-Host "`n📋 测试4：指定目标受众" -ForegroundColor Yellow
python main.py --topic "美食制作" --audience "年轻人" --count 2

Write-Host "`n✅ 所有测试完成！" -ForegroundColor Green