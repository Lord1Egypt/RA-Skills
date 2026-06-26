# SKILL.md - ddzaishot 斗地主AI助手

当你需要帮助用户玩斗地主或分析牌局时，使用此技能。

## 功能
- 🎯 识别屏幕上的牌
- 📝 自动记牌
- 🧠 AI推荐出牌
- 🖱️ 辅助出牌（可选）

## 调用方式

### 扫描屏幕识别牌局
```bash
cd ddzaishot
python src/api.py scan
```

### AI推荐出牌（需先设置牌）
```bash
# 设置我的牌和地主
python src/api.py suggest --cards=3,4,5,6,7,8,9,10,11,12,13,14,15 --landlord=me

# 演示模式（随机发牌测试）
python src/api.py demo
```

### 查看当前状态
```bash
python src/api.py status
```

## 牌值对应
- 3-10: 数字牌
- 11: J
- 12: Q
- 13: K
- 14: A
- 15: 2
- 16: 小王
- 17: 大王

## 交互式模式
```bash
python src/main.py
```
然后输入命令：
- `s` 扫描屏幕
- `p` 推荐出牌
- `m` 手动输入牌
- `l` 设置地主
- `d` 演示模式

## 注意事项
1. 屏幕识别需要先制作卡牌模板放到 `templates/` 目录
2. 鼠标控制需要先运行 `c` 命令校准
3. 建议先在演示模式下测试AI逻辑

## 依赖
```bash
pip install opencv-python numpy pyautogui pillow mss keyboard
```
