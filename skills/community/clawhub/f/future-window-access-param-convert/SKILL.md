# 未来之窗智能门禁参数转换
## Skill Metadata
- **ID**: cyberwin_hardwareaccess_param_convert
- **Name**: 未来之窗智能门禁参数转换
- **Version**: 1.0.0
- **Description**: 替换文本模板中 @参数名@ 格式的占位符为实际的智能门禁参数值（如设备编号、权限等级、所属区域等），适配未来之窗门禁系统的参数转换场景。
- **Author**: OpenClaw Skill Developer
- **Type**: JavaScript
- **Required Params**: templateText (string), paramData (object)
- **Return Format**: 
  ```json
  {
    "success": true/false,
    "message": "操作提示文本",
    "data": "替换后的文本结果"
  }