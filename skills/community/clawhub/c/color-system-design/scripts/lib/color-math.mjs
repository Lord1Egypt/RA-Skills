import { APCAcontrast, sRGBtoY } from "apca-w3";

/**
 * 归一化 Hex 颜色为小写 6 位格式（#rrggbb）
 * @param {string} hex
 * @returns {string}
 */
export function normalizeHex(hex) {
	if (typeof hex !== "string") throw new Error(`无效的颜色值: ${hex}`);
	let h = hex.trim().replace(/^#/, "").toLowerCase();
	if (/^[0-9a-f]{3}$/.test(h)) {
		h = h.split("").map((c) => c + c).join("");
	}
	if (!/^[0-9a-f]{6}$/.test(h)) {
		throw new Error(`请输入有效的 3 位或 6 位 Hex 色号（如 #007275），当前输入: ${hex}`);
	}
	return `#${h}`;
}

/**
 * @param {string} hex
 * @returns {[number, number, number]} 0-255 sRGB
 */
export function hexToRgb(hex) {
	const h = normalizeHex(hex).slice(1);
	return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16));
}

/**
 * @param {number} r 0-255
 * @param {number} g 0-255
 * @param {number} b 0-255
 * @returns {string}
 */
export function rgbToHex(r, g, b) {
	const clamp = (v) => Math.max(0, Math.min(255, Math.round(v)));
	return `#${[r, g, b].map((v) => clamp(v).toString(16).padStart(2, "0")).join("")}`;
}

const srgbToLinear = (c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const linearToSrgb = (c) => (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(Math.max(0, c), 1 / 2.4) - 0.055);

/**
 * WCAG 2.1 相对亮度
 * @param {string} hex
 * @returns {number}
 */
export function luminance(hex) {
	const [r, g, b] = hexToRgb(hex).map((v) => srgbToLinear(v / 255));
	return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/**
 * WCAG 2.1 对比度比值 (1 ~ 21)
 * @param {string} hexA
 * @param {string} hexB
 * @returns {number}
 */
export function wcagContrast(hexA, hexB) {
	const l1 = luminance(hexA);
	const l2 = luminance(hexB);
	return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
}

/**
 * APCA (WCAG 3 候选) 感知对比度 Lc 值 (-108 ~ +106)
 * 正值表示深字浅底，负值表示浅字深底
 * @param {string} textHex 前景色（文字/图标/边框）
 * @param {string} bgHex 背景色
 * @returns {number}
 */
export function apcaContrast(textHex, bgHex) {
	const txtY = sRGBtoY(hexToRgb(textHex));
	const bgY = sRGBtoY(hexToRgb(bgHex));
	const lc = APCAcontrast(txtY, bgY);
	return typeof lc === "number" ? Number(lc.toFixed(1)) : 0;
}

/**
 * Hex 转 OKLCH（Björn Ottosson 官方矩阵）
 * @param {string} hex
 * @returns {{ L: number, C: number, H: number }}
 */
export function hexToOklch(hex) {
	const [r, g, b] = hexToRgb(hex).map((v) => srgbToLinear(v / 255));
	const l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b;
	const m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b;
	const s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b;
	const l_ = Math.cbrt(l);
	const m_ = Math.cbrt(m);
	const s_ = Math.cbrt(s);
	const L = 0.2104542553 * l_ + 0.793617785 * m_ - 0.0040720468 * s_;
	const a = 1.9779984951 * l_ - 2.428592205 * m_ + 0.4505937099 * s_;
	const bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.808675766 * s_;
	let H = (Math.atan2(bb, a) * 180) / Math.PI;
	if (H < 0) H += 360;
	return { L, C: Math.hypot(a, bb), H };
}

/**
 * OKLCH 转线性 sRGB（用于判断色域内及转换）
 */
function oklchToLinearRgb(L, C, H) {
	const rad = (H * Math.PI) / 180;
	const a = C * Math.cos(rad);
	const b = C * Math.sin(rad);
	const l_ = L + 0.3963377774 * a + 0.2158037573 * b;
	const m_ = L - 0.1055613458 * a - 0.0638541728 * b;
	const s_ = L - 0.0894841775 * a - 1.291485548 * b;
	const l = l_ * l_ * l_;
	const m = m_ * m_ * m_;
	const s = s_ * s_ * s_;
	return [
		+4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
		-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
		-0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s,
	];
}

function inSrgbGamut([r, g, b]) {
	const eps = 1e-4;
	return r >= -eps && r <= 1 + eps && g >= -eps && g <= 1 + eps && b >= -eps && b <= 1 + eps;
}

/**
 * OKLCH 转 sRGB Hex（若超出 sRGB 色域，保持 L 与 H 不变，二分压缩彩度 C 至色域边界）
 * @param {number} L 0-1
 * @param {number} C >=0
 * @param {number} H 0-360
 * @returns {string}
 */
export function oklchToHex(L, C, H) {
	const clampedL = Math.max(0, Math.min(1, L));
	let rgb = oklchToLinearRgb(clampedL, C, H);
	if (!inSrgbGamut(rgb) && C > 0) {
		let lo = 0;
		let hi = C;
		for (let i = 0; i < 24; i++) {
			const mid = (lo + hi) / 2;
			if (inSrgbGamut(oklchToLinearRgb(clampedL, mid, H))) {
				lo = mid;
			} else {
				hi = mid;
			}
		}
		rgb = oklchToLinearRgb(clampedL, lo, H);
	}
	return rgbToHex(
		linearToSrgb(rgb[0]) * 255,
		linearToSrgb(rgb[1]) * 255,
		linearToSrgb(rgb[2]) * 255,
	);
}

/**
 * 两个色相角之间的最短圆周距离 (0-180)
 * @param {number} a
 * @param {number} b
 * @returns {number}
 */
export function hueDistance(a, b) {
	const d = Math.abs(a - b) % 360;
	return d > 180 ? 360 - d : d;
}

/**
 * 在 OKLCH 下固定 H 和 C，二分求解达到目标 WCAG 对比度的亮度 L
 * @param {object} opts
 * @param {string} opts.bgHex 背景色
 * @param {number} opts.targetRatio 目标 WCAG 对比度
 * @param {number} opts.H 色相
 * @param {number} opts.C 彩度
 * @param {"darker"|"lighter"} opts.direction 相对背景变暗还是变亮
 * @returns {string}
 */
export function solveLForContrast({ bgHex, targetRatio, H, C, direction }) {
	const bgL = hexToOklch(bgHex).L;
	let lo = direction === "darker" ? 0 : bgL;
	let hi = direction === "darker" ? bgL : 1;

	for (let i = 0; i < 32; i++) {
		const mid = (lo + hi) / 2;
		const hex = oklchToHex(mid, C, H);
		const ratio = wcagContrast(hex, bgHex);
		if (direction === "darker") {
			// L 越小越暗，对比度越大
			if (ratio >= targetRatio) {
				lo = mid;
			} else {
				hi = mid;
			}
		} else {
			// L 越大越亮，对比度越大
			if (ratio >= targetRatio) {
				hi = mid;
			} else {
				lo = mid;
			}
		}
	}
	return oklchToHex(direction === "darker" ? lo : hi, C, H);
}
