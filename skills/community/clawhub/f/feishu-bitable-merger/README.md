# 飞书多维表格合并工具 📊

一个强大的飞书多维表格数据合并工具，可以快速合并多个表格的数据到一个目标表格。

## 功能特点
- ✅ 自动匹配相同字段名称
- ✅ 支持自定义字段映射
- ✅ 支持合并后去重
- ✅ 批量处理，支持大数据量
- ✅ 保留原始数据格式
- ✅ 增量合并支持

## 安装
```bash
clawhub install feishu-bitable-merger
```

## 使用方法

### 基本合并
合并多个表格到目标表格：
```bash
feishu-bitable-merger merge \
  --source "https://example.com/base/xxx1?table=yyy1" "https://example.com/base/xxx2?table=yyy2" \
  --target "https://example.com/base/xxx3?table=yyy3"
```

### 带字段映射合并
当源表格和目标表格字段名称不一致时，可以使用字段映射：
```bash
feishu-bitable-merger merge \
  --source "source1" "source2" \
  --target "target" \
  --map "客户名称:客户" "订单金额:金额"
```

### 合并后去重
添加 `--deduplicate` 参数自动去重完全相同的记录：
```bash
feishu-bitable-merger merge \
  --source "source1" "source2" \
  --target "target" \
  --deduplicate
```

## 权限要求
使用前需要确保飞书应用有以下权限：
- `bitable:app:read` - 读取多维表格
- `bitable:app:write` - 写入多维表格
- `bitable:record:read` - 读取记录
- `bitable:record:write` - 写入记录

## 使用场景
1. 合并多个部门提交的报表数据
2. 汇总不同时间段的统计数据
3. 整合多个数据源到统一表格
4. 数据迁移和备份

## 注意事项
- 目标表格需要预先创建好对应的字段
- 字段类型需要匹配，否则可能写入失败
- 单次合并最多支持 10000 条记录
- 建议先在测试表格上验证再正式使用

## 许可证
MIT
