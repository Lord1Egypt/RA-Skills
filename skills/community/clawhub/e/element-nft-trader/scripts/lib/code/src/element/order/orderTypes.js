"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SignatureType = exports.MAX_LISTING_TIME = exports.MAX_EXPIRATION_TIME = exports.DEFAULT_EXPIRATION_TIME = void 0;
exports.DEFAULT_EXPIRATION_TIME = (7 * 86400);
exports.MAX_EXPIRATION_TIME = (365 * 86400);
exports.MAX_LISTING_TIME = (365 * 86400);
var SignatureType;
(function (SignatureType) {
    SignatureType[SignatureType["EIP712"] = 0] = "EIP712";
    SignatureType[SignatureType["PRESIGNED"] = 1] = "PRESIGNED";
})(SignatureType || (exports.SignatureType = SignatureType = {}));
//# sourceMappingURL=orderTypes.js.map