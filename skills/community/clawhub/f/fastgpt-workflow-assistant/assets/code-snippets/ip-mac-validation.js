/**
 * IP/MAC 地址校验标准代码片段
 * 用于 FastGPT 代码节点（JavaScript）的输入合法性校验。
 * 拒绝 0.0.0.0、255.255.255.255、环回、链路本地、组播和保留段地址。
 */
function validateIp(ip) {
  if (typeof ip !== "string" || !ip) {
    return { valid: false, reason: "IP为空" };
  }
  const parts = ip.split(".");
  if (parts.length !== 4) {
    return { valid: false, reason: "IP格式不是四段" };
  }
  const octets = [];
  for (let i = 0; i < 4; i++) {
    const seg = parts[i];
    if (!/^\d+$/.test(seg)) {
      return { valid: false, reason: `第${i + 1}段含非数字字符` };
    }
    const num = Number(seg);
    if (num < 0 || num > 255) {
      return { valid: false, reason: `第${i + 1}段越界` };
    }
    octets.push(num);
  }
  const [a, b, c, d] = octets;
  if (a === 0 && b === 0 && c === 0 && d === 0) {
    return { valid: false, reason: "禁止0.0.0.0" };
  }
  if (a === 255 && b === 255 && c === 255 && d === 255) {
    return { valid: false, reason: "禁止255.255.255.255" };
  }
  if (a === 127) {
    return { valid: false, reason: "禁止环回地址" };
  }
  if (a === 169 && b === 254) {
    return { valid: false, reason: "禁止链路本地地址" };
  }
  if (a >= 224) {
    return { valid: false, reason: "禁止组播或保留段地址" };
  }
  return { valid: true, reason: "" };
}

function validateMac(mac) {
  if (typeof mac !== "string" || !mac) {
    return { valid: false, reason: "MAC为空" };
  }
  const cleaned = mac.replace(/[\s:-]/g, "").toUpperCase();
  if (!/^[0-9A-F]{12}$/.test(cleaned)) {
    return { valid: false, reason: "MAC应为12位十六进制" };
  }
  const firstByte = parseInt(cleaned.substring(0, 2), 16);
  if ((firstByte & 0x01) === 1) {
    return { valid: false, reason: "禁止组播MAC" };
  }
  if (cleaned === "000000000000") {
    return { valid: false, reason: "禁止全零MAC" };
  }
  if (cleaned === "FFFFFFFFFFFF") {
    return { valid: false, reason: "禁止广播MAC" };
  }
  return { valid: true, reason: "" };
}

async function main({ params }) {
  const ipResult = validateIp(params.ip);
  const macResult = validateMac(params.mac);
  if (!ipResult.valid || !macResult.valid) {
    return {
      finalText: `输入不合法：${ipResult.reason || macResult.reason}`,
      retry: true
    };
  }
  return { finalText: "", retry: false };
}
