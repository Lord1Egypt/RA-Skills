# 01-entry-and-arg-parsing.md

## 目标
解析用户是否明确提供了：
- 楼盘名称
- 模式参数
- 平台参数

## 规则
1. 没有楼盘名称时，只追问楼盘名称。
2. 有楼盘名称时，默认：
   - mode=auto
   - platform=moments
3. 不要在参数不完整时提前生成文案。
