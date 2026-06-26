// src/core/env-checker.js

/**
 * EnvChecker: 环境指纹捕获器
 * 确保捕获的指纹完全符合 AEIF 1.0 Schema 规范
 */
class EnvChecker {
  static getFingerprint() {
    return {
      os: process.platform,          // e.g., 'darwin', 'linux', 'win32'
      arch: process.arch,            // e.g., 'x64', 'arm64'
      runtime: `node@${process.version}`, // 必须符合 AEIF 1.0: "node@v18.x"
      compatibility: "cross-platform",   // 默认先设为跨平台，由提炼器后期修正
      env: process.env.NODE_ENV || 'development',
      dependencies: {} // 可选：后续可扩展读取 package.json
    };
  }

  /**
   * 评估 Capsule 在当前环境的兼容性
   */
  static checkCompatibility(capsule, currentEnv = EnvChecker.getFingerprint()) {
    const capEnv = capsule.environment;

    if (capEnv.compatibility === 'cross-platform') {
      return { compatible: true, confidence: 1.0 };
    }

    if (capEnv.os !== 'any' && capEnv.os !== currentEnv.os) {
      return {
        compatible: false,
        warning: `This solution was verified on ${capEnv.os}, current is ${currentEnv.os}.`,
        confidence: 0.4
      };
    }

    return { compatible: true, confidence: 0.85 };
  }
}

module.exports = EnvChecker;
