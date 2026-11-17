"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.requireProcessingApproval = requireProcessingApproval;
const types_1 = require("./types");
const i18n_1 = require("./i18n");
const outboundActions = new Set(['uploadVideo', 'submitTask', 'removeVideoWatermark', 'removeImageWatermark', 'workflow']);
// Explicit acknowledgement is checked before file access or network effects.
// It records host/user consent; it is not a substitute for the host's approval UI.
function requireProcessingApproval(action, params = {}) {
    if (!outboundActions.has(action) || params.confirmProcessing === true)
        return null;
    return { code: types_1.ErrorCode.INVALID_PARAMS, message: (0, i18n_1.localize)(params.locale, '请先向用户说明所选素材或链接将发送至 550W，处理可能扣除积分；用户确认本次操作后传入 confirmProcessing=true。', 'Explain that selected media or links will be sent to 550W and processing may spend credits. Set confirmProcessing=true only after the user approves this operation.') };
}
//# sourceMappingURL=processing-approval.js.map