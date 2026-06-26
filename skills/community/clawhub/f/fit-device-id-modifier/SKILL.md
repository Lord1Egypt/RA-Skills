# fit-device-id-modifier

修改 FIT 文件的设备 ID（manufacturer 和 garmin_product），将骑行记录转换为 Garmin Edge 500 China 设备生成的格式。

## 用途

- 修改 FIT 文件中的 `manufacturer` 字段为 `1` (Garmin)
- 修改 `garmin_product` 字段为 `1030` (Edge 500 China)
- 用于让第三方骑行软件生成的 FIT 文件能被 Garmin Connect 等平台正确识别

## 依赖

- Python 3.x
- `fitparse` 库 (`pip install fitparse`)

## 使用方法

### 批量处理子目录中的 FIT 文件

```bash
cd /home/ckboss/.openclaw/workspace/skills/fit-device-id-modifier/scripts
/home/ckboss/anaconda3/bin/python modify_fit.py
```

这会处理 `./ */*.fit` 匹配的所有 FIT 文件，生成 `_GM.fit` 后缀的修改版。

### 处理单个文件

```bash
/home/ckboss/anaconda3/bin/python modify_fit.py /path/to/ride.fit
```

### 处理整个目录

```bash
/home/ckboss/anaconda3/bin/python modify_fit.py /path/to/rides/
```

## 输出

- 原文件保持不变
- 生成新文件：`原文件名_GM.fit`

## 注意事项

- 会自动跳过已处理的文件（文件名包含 `_GM.fit`）
- 会重新计算 CRC 校验和确保文件完整性
- 使用 conda Python：`/home/ckboss/anaconda3/bin/python`

## 文件结构

```
skills/fit-device-id-modifier/
├── SKILL.md
└── scripts/
    └── modify_fit.py
```
