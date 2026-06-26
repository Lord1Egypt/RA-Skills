# # 导出多组数据到通达信客户端 print_to_tdx

### # 将计算数据导出到通达信客户端展示

```python
print_to_tdx(df_list:          list[pd.DataFrame] = [],
			sp_name:          str  = "",
			xml_filename:     str  = "",
			jsn_filenames:    list[str] = None,
			vertical:         int  = None,
			horizontal:       int  = None,
			height:           list[str | float] = None,
			table_names:      list[str] = None) -> None:
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| df_list | Y | list[pd.DataFrame] | 多组数据的DataFrame列表，每组table对应1个DataFrame；每个DataFrame非空且第一列为日期（datetime64[ns]或字符串类型），后续列为指标/因子名称；列表长度需等于组数 |
| sp_name | N | str | 生成.sp文件的名称前缀，为空时默认生成python.sp |
| xml_filename | N | str | 生成的xml文件名（需包含.xml后缀），为空会影响通达信面板配置关联，建议必填 |
| jsn_filenames | Y | list[str] | 每组数据对应的.jsn文件名列表，列表非空且长度需等于组数（与df_list一致），文件名建议包含.jsn后缀 |
| vertical | N | int | 纵向排列的table组数（≥1），与horizontal二选一，horizontal优先级更高 |
| horizontal | N | int | 横向排列的table组数（≥1），优先级高于vertical，未指定时默认使用vertical或1组 |
| height | N | list[str \| float] | 自定义每组gridctrl高度列表，长度需等于组数；元素为数值/字符串（高度占比），未指定时自动计算（1/组数，最后一组高度为0） |
| table_names | N | list[str] | 每组展示面板的标题列表，长度需等于组数；元素为空时自动使用对应jsn_filenames的前缀作为标题 |

- df_list、jsn_filenames长度必须与vertical/horizontal指定的组数完全一致，否则会抛出ValueError异常
- height参数值为高度占比（如0.3/"0.3"），表示该面板占整体展示区域的比例，仅支持0-1之间的数值
- 未指定vertical/horizontal时，默认按1组纵向排列展示，自动计算面板高度
