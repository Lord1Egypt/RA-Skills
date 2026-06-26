# ddzaishot - 斗地主AI助手 💎

**功能：**
- 🎯 屏幕识别：识别三家的牌
- 📝 记牌器：自动记录出牌历史
- 🧠 AI分析：推测剩余手牌，推荐出牌策略
- 🖱️ 辅助操作：鼠标点击出牌

---

## 快速开始

```bash
cd ddzaishot
pip install -r requirements.txt
python src/main.py
```

## 使用方法

1. 打开斗地主游戏
2. 运行 `python src/main.py`
3. AI会自动识别屏幕，帮你记牌和推荐出牌

---

## 项目结构

```
ddzaishot/
├── src/
│   ├── main.py          # 主程序入口
│   ├── screen.py        # 屏幕截图和识别
│   ├── cards.py         # 牌的识别和管理
│   ├── game.py          # 游戏状态管理
│   ├── ai.py            # AI决策引擎
│   └── mouse.py         # 鼠标控制
├── templates/           # 卡牌模板图片
├── models/              # AI模型（可选）
└── logs/                # 游戏记录
```

## 操作命令

- `s` - 截图识别当前状态
- `r` - 重置游戏
- `h` - 显示帮助
- `q` - 退出
