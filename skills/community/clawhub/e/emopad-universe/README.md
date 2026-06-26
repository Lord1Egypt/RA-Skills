# emoPAD-universe
openclaw skill to use multi-modal signals to display real-time emotion PAD coordinates and recent emotion nebula

情绪宇宙技能 - 帮助用户在情绪 PAD（Pleasure-Arousal-Dominance）坐标系中定位情绪。

## 自动启动

**安装此skill后，会自动启动emoPAD服务和emoNebula自动报告，无需手动操作。**

安装时会自动：
1. 检查并安装所需的Python依赖
2. 启动emoPAD服务（监听 http://127.0.0.1:8766）
3. 启动emoNebula自动报告（每5分钟发送一次情绪星云图）

## 功能

- **emoNebula**: 持续实时监测情绪 PAD，每隔 5 分钟生成并发送情绪星云图
- **实时状态**: 随时获取当前情绪 PAD 和传感器连接状态
- **手动截图**: 随时生成情绪星云图

[▶️ 在 Bilibili 观看演示](https://www.bilibili.com/video/BV1QKPUz7EHV/?spm_id_from=333.337.search-card.all.click)

## 支持的硬件

| 类型 | 型号 | 连接方式 |
|------|------|----------|
| EEG | KSEEG102 | 蓝牙 BLE |
| PPG | Cheez PPG 传感器 | 串口 |
| GSR | Sichiray GSR V2 | 串口 |

## 使用

```bash
openclaw emopad status     # 获取当前 PAD 状态
openclaw emopad snapshot   # 手动生成情绪星云图
openclaw emopad stop       # 停止服务
openclaw emopad start      # 重新启动服务
```

## 重要说明

**关于情绪 PAD 计算**: 目前是基于启发式方法，根据大量文献总结得出的映射关系。这种方法暂时无法体现个性化差异。未来版本将加入个性化校准训练模块，真正实现个性化情绪识别。
