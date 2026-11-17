"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.assertPublicVideoUrl = assertPublicVideoUrl;
exports.probeVideoUrl = probeVideoUrl;
const child_process_1 = require("child_process");
const dns_1 = require("dns");
const net_1 = require("net");
function isBlockedAddress(address) {
    const value = address.toLowerCase();
    if (value === "::1" || value === "::" || value.startsWith("fc") || value.startsWith("fd") || value.startsWith("ff") || /^fe[89ab]/.test(value))
        return true;
    const mapped = value.match(/^::ffff:(\d+\.\d+\.\d+\.\d+)$/)?.[1];
    const ipv4 = mapped || ((0, net_1.isIP)(value) === 4 ? value : null);
    if (!ipv4)
        return false;
    const [a, b] = ipv4.split(".").map(Number);
    return a === 0 || a === 10 || a === 127 || a >= 224
        || (a === 100 && b >= 64 && b <= 127)
        || (a === 169 && b === 254)
        || (a === 172 && b >= 16 && b <= 31)
        || (a === 192 && (b === 0 || b === 168))
        || (a === 198 && (b === 18 || b === 19 || b === 51))
        || (a === 203 && b === 0);
}
async function assertPublicVideoUrl(videoUrl) {
    const parsed = new URL(videoUrl);
    if (!['http:', 'https:'].includes(parsed.protocol) || parsed.username || parsed.password) {
        throw new Error("Only unauthenticated public HTTP(S) video URLs are allowed");
    }
    const hostname = parsed.hostname.toLowerCase();
    if (hostname === "localhost" || hostname.endsWith(".localhost") || hostname.endsWith(".local") || hostname.endsWith(".internal")) {
        throw new Error("Local and private video URLs are not allowed");
    }
    const addresses = (0, net_1.isIP)(hostname) ? [{ address: hostname }] : await dns_1.promises.lookup(hostname, { all: true, verbatim: true });
    if (addresses.length === 0 || addresses.some(({ address }) => isBlockedAddress(address))) {
        throw new Error("The video URL must resolve only to public network addresses");
    }
}
/**
 * 使用本机 ffprobe 获取远程视频的真实元信息。不得伪造默认宽高和时长：这些字段既参与
 * 服务端快速拒绝，也可能在远程媒体暂时无法探测时成为兜底依据。
 */
async function probeVideoUrl(videoUrl) {
    await assertPublicVideoUrl(videoUrl);
    const ffprobe = process.env.FFPROBE_PATH?.trim() || "ffprobe";
    const args = [
        "-v", "error",
        "-protocol_whitelist", "http,https,tcp,tls",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height:format=duration",
        "-of", "json",
        videoUrl,
    ];
    return new Promise((resolve, reject) => {
        (0, child_process_1.execFile)(ffprobe, args, { timeout: 20000, maxBuffer: 1024 * 1024 }, (error, stdout) => {
            if (error) {
                reject(new Error(`无法预检远程视频，请确认链接可访问且已安装 ffprobe：${error.message}`));
                return;
            }
            try {
                const payload = JSON.parse(stdout);
                const stream = payload?.streams?.[0];
                const width = Number(stream?.width);
                const height = Number(stream?.height);
                const duration = Math.ceil(Number(payload?.format?.duration));
                if (!Number.isFinite(width) || !Number.isFinite(height) || !Number.isFinite(duration)
                    || width <= 0 || height <= 0 || duration <= 0) {
                    throw new Error("未读取到有效的视频宽高或时长");
                }
                resolve({ width, height, duration });
            }
            catch (parseError) {
                reject(new Error(`远程视频预检结果无效：${parseError?.message || "未知错误"}`));
            }
        });
    });
}
//# sourceMappingURL=video-probe.js.map