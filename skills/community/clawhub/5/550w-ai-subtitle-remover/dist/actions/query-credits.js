"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.queryCredits = queryCredits;
const validator_1 = require("../validator");
const error_handler_1 = require("../error-handler");
const types_1 = require("../types");
async function queryCredits(params, client) {
    const apiResponse = await client.post("/open/queryCredits", {}, types_1.TIMEOUT_CONFIG.query);
    if (apiResponse.code !== types_1.ErrorCode.SUCCESS) {
        return (0, error_handler_1.mapApiError)(apiResponse);
    }
    const result = {
        code: types_1.ErrorCode.SUCCESS,
        message: "查询成功",
        userNo: apiResponse.userNo,
        credits: apiResponse.credits,
    };
    if (params.width !== undefined || params.height !== undefined || params.duration !== undefined) {
        const estimateError = (0, validator_1.validate)("estimateCredits", params);
        if (estimateError)
            return estimateError;
        result.estimation = (0, validator_1.estimateCredits)(params.width, params.height, params.duration);
    }
    return result;
}
//# sourceMappingURL=query-credits.js.map