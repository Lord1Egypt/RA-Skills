# Testing Reference

## pytest依赖

执行测试前需要安装pytest：

```bash
pip3 install pytest --break-system-packages
```

## 测试文件位置

```
tests/
├── test_interceptor.py    # interceptor.py测试
└── test_trust_tracker.py   # trust_tracker.py测试
```

## 运行测试

```bash
# 运行所有测试
python3 -m pytest tests/ -v

# 运行单个文件
python3 -m pytest tests/test_interceptor.py -v
```

## 测试原则

- 每个测试函数测试一个场景
- 测试函数命名：`test_<场景描述>`
- 断言要明确，失败时能快速定位问题
