/**
 * OpenClaw 标准技能：未来之窗智能门禁参数转换
 * Skill ID: cyberwin_hardwareaccess_param_convert
 * Version: 1.0.0
 */
$claw.skill({
    // 技能元信息（与SKILL.md严格一致）
    name: "未来之窗智能门禁参数转换",
    id: "cyberwin_hardwareaccess_param_convert",
    version: "1.0.0",
    desc: "替换文本模板中 @参数名@ 格式的占位符为实际的智能门禁参数值",
    
    // 入参定义（平台规范要求，明确入参类型/必填项/说明）
    params: [
        {
            name: "templateText",
            type: "string",
            required: true,
            desc: "包含@参数名@占位符的门禁文本模板"
        },
        {
            name: "paramData",
            type: "object",
            required: true,
            desc: "门禁参数键值对（如：{deviceId: 'WC001', level: '管理员'}）"
        }
    ],
    
    // 技能核心执行逻辑
    handler: function (args) {
        try {
            // 1. 入参校验，避免非法入参导致报错
            const { templateText, paramData } = args;
            if (!templateText || typeof templateText !== 'string') {
                return {
                    success: false,
                    message: "入参错误：templateText必须为非空字符串",
                    data: ""
                };
            }
            if (!paramData || typeof paramData !== 'object' || Array.isArray(paramData)) {
                return {
                    success: false,
                    message: "入参错误：paramData必须为非数组的对象类型",
                    data: ""
                };
            }

            // 2. 核心逻辑：替换@参数名@格式的占位符
            const placeholderReg = /@(\w+)@/g;
            const resultText = templateText.replace(placeholderReg, function (match, key) {
                // 有对应参数则替换，无则保留原占位符
                return paramData.hasOwnProperty(key) ? paramData[key] : match;
            });

            // 3. 返回平台标准格式的成功结果
            return {
                success: true,
                message: "门禁参数转换成功",
                data: resultText
            };
        } catch (error) {
            // 异常捕获，返回标准化错误信息
            return {
                success: false,
                message: `门禁参数转换失败：${error.message}`,
                data: ""
            };
        }
    }
});