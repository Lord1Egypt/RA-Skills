"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.openSelectedLocalMedia = openSelectedLocalMedia;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const types_1 = require("./types");
function openSelectedLocalMedia(filePath, kind) {
    const absolutePath = path.resolve(filePath);
    const stat = fs.lstatSync(absolutePath);
    if (stat.isSymbolicLink() || !stat.isFile()) {
        throw new Error("filePath must point directly to a regular file, not a symbolic link");
    }
    const extension = path.extname(absolutePath).toLowerCase();
    const extensions = kind === "video" ? types_1.SUPPORTED_VIDEO_EXTENSIONS : types_1.SUPPORTED_IMAGE_EXTENSIONS;
    const maxSize = kind === "video" ? types_1.MAX_FILE_SIZE : types_1.MAX_IMAGE_FILE_SIZE;
    if (!extensions.includes(extension))
        throw new Error(`Unsupported ${kind} file extension`);
    if (stat.size > maxSize)
        throw new Error(`${kind} file exceeds the size limit`);
    return {
        name: path.basename(absolutePath),
        size: stat.size,
        data: fs.createReadStream(absolutePath),
    };
}
//# sourceMappingURL=local-media.js.map