// src/storage/validator.js
const Ajv = require("ajv");
const addFormats = require("ajv-formats");
const schema = require("../config/aeif-schema.json");

class AEIFValidator {
    constructor() {
        // allErrors: true 为了收集更多调试信息, useDefaults: true 自动填充 Schema 中的默认值
        const ajv = new Ajv({ allErrors: true, useDefaults: true });
        addFormats(ajv);
        this.validate = ajv.compile(schema);
    }

    /**
     * 断言数据合法性
     * @param {Object} capsule - AEIF 经验胶囊对象
     * @returns {boolean}
     * @throws {Error} 校验失败时抛出详细结构化错误
     */
    assertValid(capsule) {
        const isValid = this.validate(capsule);
        if (!isValid) {
            // 提供结构化、开发者易读的错误报告
            const errors = this.validate.errors
                .map(e => `[${e.instancePath || 'root'}] ${e.message} (value: ${JSON.stringify(e.data)})`)
                .join('; ');
            throw new Error(`[AEIF Violation] Invalid experience capsule format: ${errors}`);
        }
        return true;
    }
}

module.exports = { AEIFValidator };
