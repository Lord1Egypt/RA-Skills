"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.EnvManager = void 0;
const path_1 = __importDefault(require("path"));
const fs_1 = require("../common/fs");
class EnvManager {
    constructor() {
        this.MIRRORS = {
            GITHUB: 'https://github.com/espressif/esp-idf.git',
            GITEE: 'https://gitee.com/EspressifSystems/esp-idf.git',
            CDN_ASSETS: 'https://dl.espressif.cn/github_assets'
        };
    }
    /**
     * 返回静态的手动安装建议，不在 skill 内主动联网测速
     */
    async installIDF(targetPath, version = 'v5.3') {
        return {
            status: 'MANUAL_INSTALL_REQUIRED',
            path: targetPath,
            version,
            options: {
                github: {
                    repository: this.MIRRORS.GITHUB,
                    commands: [
                        `git clone --recursive -b ${version} ${this.MIRRORS.GITHUB} ${targetPath}`,
                        `cd ${targetPath} && ./install.sh`
                    ]
                },
                gitee: {
                    repository: this.MIRRORS.GITEE,
                    mirrorAssets: this.MIRRORS.CDN_ASSETS,
                    commands: [
                        `git clone --recursive -b ${version} ${this.MIRRORS.GITEE} ${targetPath}`,
                        `cd ${targetPath} && export IDF_GITHUB_ASSETS=${this.MIRRORS.CDN_ASSETS} && ./install.sh`
                    ]
                }
            },
            suggestion: '建议先使用 manage_env({ action: "check" }) 确认本地环境状态；若确需安装，请手动选择 GitHub 或 Gitee 路径执行官方安装脚本。'
        };
    }
    /**
     * 环境嗅探：检查现有 IDF 状态
     */
    async checkExistingEnv() {
        const pythonAvailable = await this.checkCommandAvailable('python3')
            || await this.checkCommandAvailable('python');
        const idfPyAvailable = await this.checkCommandAvailable('idf.py');
        const homeDir = process.env.HOME || process.env.USERPROFILE;
        if (process.env.IDF_PATH) {
            return {
                status: 'READY',
                path: process.env.IDF_PATH,
                pythonAvailable,
                idfPyAvailable
            };
        }
        const commonPaths = [
            homeDir ? path_1.default.join(homeDir, 'esp', 'esp-idf') : undefined,
            'C:\\esp\\esp-idf'
        ].filter((value) => Boolean(value));
        for (const candidate of commonPaths) {
            if (await (0, fs_1.pathExists)(candidate)) {
                return {
                    status: 'FOUND_NOT_EXPORTED',
                    path: candidate,
                    pythonAvailable,
                    idfPyAvailable
                };
            }
        }
        return {
            status: 'NOT_FOUND',
            pythonAvailable,
            idfPyAvailable
        };
    }
    async checkCommandAvailable(command) {
        const pathValue = process.env.PATH;
        if (!pathValue) {
            return false;
        }
        const extensions = process.platform === 'win32'
            ? (process.env.PATHEXT || '.EXE;.CMD;.BAT;.COM')
                .split(';')
                .filter(Boolean)
            : [''];
        for (const dir of pathValue.split(path_1.default.delimiter)) {
            if (!dir)
                continue;
            for (const extension of extensions) {
                const candidate = process.platform === 'win32' && extension
                    ? path_1.default.join(dir, `${command}${extension}`)
                    : path_1.default.join(dir, command);
                if (await (0, fs_1.pathExists)(candidate)) {
                    return true;
                }
            }
        }
        return false;
    }
}
exports.EnvManager = EnvManager;
//# sourceMappingURL=index.js.map