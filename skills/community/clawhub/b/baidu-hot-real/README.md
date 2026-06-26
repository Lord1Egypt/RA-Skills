# 百度热搜榜 - 真实数据版 (baidu-hot-real)

## 快速开始

```bash
# 获取 Top 10
python3 scripts/baidu_real.py 10

# 获取 Top 50
python3 scripts/baidu_real.py all
```

## 特性

- ✅ **100% 真实数据** - 直接从百度热搜官网抓取
- ✅ **实时更新** - 与百度官方同步
- ✅ **热点标记** - 识别"热"、"新"等标记
- ✅ **无需 API** - 不依赖第三方 API

## 与 baidu-hot-cn 对比

| 特性 | baidu-hot-cn | baidu-hot-real |
|------|--------------|----------------|
| 数据源 | 百度 API | 百度官网 |
| 真实性 | ⚠️ 可能返回模拟数据 | ✅ 100% 真实 |
| 推荐度 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 依赖

- Python 3.x
- requests（可选，有备选方案）

## 作者

iph0n3

## 许可证

MIT
