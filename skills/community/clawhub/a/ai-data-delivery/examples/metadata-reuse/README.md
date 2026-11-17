# 从已有元数据起步

此为合成输入，不是已确认的交通行业本体。已有两张表及 vehicle_company 关系；企业当前记录数使用 COUNT(*)，不能自动等同于企业去重数。

在仓库根目录执行：

```bash
python scripts/derive_ontology.py --model examples/metadata-reuse/metadata.yaml --out tmp-candidate.yaml
python scripts/check_model.py -f tmp-candidate.yaml
python scripts/derive_ontology.py --model tmp-candidate.yaml --out tmp-repeat.yaml
python scripts/export_exchange.py --model tmp-candidate.yaml --out tmp-handoff
```

重复生成应为零新增，两个候选模型内容相同。模型 lint 可能仍有描述/枚举/时间能力等提示，按当前问题判断，不能用填假值来消除。导出仅是带摘要的候选交付，不代表语义或真实数据已验证。

工作台可导入同一文件，再点击“语义建模→从元数据补充语义草案”，编辑关系含义后重新打开、再次生成，人工内容应保留。不要再录入另一条反向关系。没有数据库与实际消费者时，不填写假的联调通过。
