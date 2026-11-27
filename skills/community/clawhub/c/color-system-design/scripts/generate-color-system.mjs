import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { BackgroundColor, Color, Theme } from "@adobe/leonardo-contrast-colors";
import {
	apcaContrast,
	hexToOklch,
	hueDistance,
	normalizeHex,
	oklchToHex,
	solveLForContrast,
	wcagContrast,
} from "./lib/color-math.mjs";
import { renderHtmlReport } from "./lib/render-html-report.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

/**
 * 解析 CLI 参数
 */
function parseArgs(argv) {
	const args = {
		seed: null,
		name: null,
		tint: "subtle",
		out: path.join(ROOT, "dist"),
		writeTokens: false,
		withSemantic: true,
	};
	for (let i = 0; i < argv.length; i++) {
		const arg = argv[i];
		if (!arg.startsWith("--") && !args.seed) {
			args.seed = arg;
		} else if (arg === "--seed" && argv[i + 1]) {
			args.seed = argv[++i];
		} else if (arg === "--name" && argv[i + 1]) {
			args.name = argv[++i];
		} else if (arg === "--tint" && argv[i + 1]) {
			args.tint = argv[++i];
		} else if (arg === "--out" && argv[i + 1]) {
			args.out = path.resolve(argv[++i]);
		} else if (arg === "--write-tokens") {
			args.writeTokens = true;
		} else if (arg === "--no-semantic") {
			args.withSemantic = false;
		} else if (arg === "--help" || arg === "-h") {
			printHelp();
			process.exit(0);
		}
	}
	return args;
}

function printHelp() {
	console.log(`
用法:
  pnpm generate -- --seed "#007275" [选项]
  node scripts/generate-color-system.mjs "#007275" [选项]

选项:
  --seed <hex>       必需，单个基础品牌色（3位或6位 Hex，如 #007275）
  --name <slug>      方案名称（默认使用色号命名）
  --tint <mode>      中性灰倾向: subtle(默认,微带主色) | pure(纯灰) | warm(暖纸) | cool(冷纸)
  --out <dir>        输出目录（默认 ./dist）
  --write-tokens     同时更新根目录 tokens/ 下的 DTCG 真源 JSON
  --no-semantic      仅生成核心 danger 危险色，不生成 success/warning/info 扩展异色
  -h, --help         显示帮助
`);
}

/**
 * 确定中性阶的 OKLCH 色相与彩度（依据：Material HCT Tinted Neutrals + OKLCH 低彩度约束 C ≤ 0.012）
 */
function resolveNeutralConfig(seedOklch, tintMode) {
	switch (tintMode) {
		case "pure":
			return { hue: 0, paperC: 0, midC: 0 };
		case "warm":
			return { hue: 65, paperC: 0.005, midC: 0.008 };
		case "cool":
			return { hue: 225, paperC: 0.005, midC: 0.008 };
		case "subtle":
		default:
			return {
				hue: Number(seedOklch.H.toFixed(2)),
				paperC: Math.min(0.006, seedOklch.C * 0.08),
				midC: Math.min(0.01, seedOklch.C * 0.12),
			};
	}
}

/**
 * 用 Leonardo 计算强调色阶（固定纸面背景，不让纸色漂移）
 */
function solveLeonardoAccent(paperHex, seedHex, ratios) {
	const bg = new BackgroundColor({
		name: "paper",
		colorKeys: [paperHex],
		ratios: [1],
	});
	const accent = new Color({
		name: "accent",
		colorKeys: [seedHex],
		colorSpace: "CAM02",
		ratios,
		smooth: true,
	});
	const lStar = Math.max(4, Math.min(98, Math.round(hexToOklch(paperHex).L > 0.5 ? 97 : 6)));
	const theme = new Theme({
		colors: [accent],
		backgroundColor: bg,
		lightness: lStar,
		contrast: 1,
		output: "HEX",
	});
	const values = theme.contrastColors[1]?.values ?? [];
	return values.map((v) => v.value.toLowerCase());
}

/**
 * 避开主强调色的状态色相求解（确保异色与主色在视觉上明确分离）
 */
function pickSeparatedHue(preferredHue, seedHue, minGap = 35) {
	if (hueDistance(preferredHue, seedHue) >= minGap) return preferredHue;
	const plus = (preferredHue + minGap) % 360;
	const minus = (preferredHue - minGap + 360) % 360;
	return hueDistance(plus, seedHue) >= hueDistance(minus, seedHue) ? plus : minus;
}

/**
 * 生成完整色彩系统数据
 */
export function generateColorSystem({
	seed,
	name = null,
	tint = "subtle",
	withSemantic = true,
}) {
	const seedHex = normalizeHex(seed);
	const seedOklch = hexToOklch(seedHex);
	const slug = name || `seed-${seedHex.slice(1)}`;
	const neutralCfg = resolveNeutralConfig(seedOklch, tint);

	// 1. 中性阶求解（亮色 & 暗色）
	const lightPaper = oklchToHex(0.976, neutralCfg.paperC, neutralCfg.hue);
	const darkPaper = oklchToHex(0.175, neutralCfg.paperC, neutralCfg.hue);

	const lightNeutral = {
		"0": lightPaper,
		"100": solveLForContrast({ bgHex: lightPaper, targetRatio: 1.09, H: neutralCfg.hue, C: neutralCfg.midC, direction: "darker" }),
		"200": solveLForContrast({ bgHex: lightPaper, targetRatio: 1.46, H: neutralCfg.hue, C: neutralCfg.midC, direction: "darker" }),
		"300": solveLForContrast({ bgHex: lightPaper, targetRatio: 3.25, H: neutralCfg.hue, C: neutralCfg.midC, direction: "darker" }),
		"400": solveLForContrast({ bgHex: lightPaper, targetRatio: 5.35, H: neutralCfg.hue, C: neutralCfg.midC, direction: "darker" }),
		"900": solveLForContrast({ bgHex: lightPaper, targetRatio: 16.5, H: neutralCfg.hue, C: neutralCfg.midC * 0.6, direction: "darker" }),
	};

	const darkNeutral = {
		"0": darkPaper,
		"100": solveLForContrast({ bgHex: darkPaper, targetRatio: 1.12, H: neutralCfg.hue, C: neutralCfg.midC, direction: "lighter" }),
		"200": solveLForContrast({ bgHex: darkPaper, targetRatio: 1.45, H: neutralCfg.hue, C: neutralCfg.midC, direction: "lighter" }),
		"300": solveLForContrast({ bgHex: darkPaper, targetRatio: 3.85, H: neutralCfg.hue, C: neutralCfg.midC, direction: "lighter" }),
		"400": solveLForContrast({ bgHex: darkPaper, targetRatio: 7.2, H: neutralCfg.hue, C: neutralCfg.midC, direction: "lighter" }),
		"900": solveLForContrast({ bgHex: darkPaper, targetRatio: 15.2, H: neutralCfg.hue, C: neutralCfg.midC * 0.6, direction: "lighter" }),
	};

	// 2. 深图版底色（两主题均保持深底，供封面/深色卡片/Hero 使用）
	const lightDeep = oklchToHex(0.19, Math.min(0.015, seedOklch.C * 0.15), seedOklch.H);
	const darkDeep = oklchToHex(0.13, Math.min(0.015, seedOklch.C * 0.15), seedOklch.H);

	// 3. Leonardo 强调色阶
	// 亮色种子：保证足够彩度；暗色种子：构造同色相高亮高彩种子避免暗背景发灰
	const lightLeoSeed = oklchToHex(Math.min(0.55, Math.max(0.35, seedOklch.L)), Math.max(0.08, seedOklch.C), seedOklch.H);
	const darkLeoSeed = oklchToHex(0.76, Math.max(0.11, Math.min(0.18, seedOklch.C * 1.1)), seedOklch.H);

	const [lightAccent100, lightAccent200] = solveLeonardoAccent(lightPaper, lightLeoSeed, [4.85, 5.85]);
	const [darkAccent100, darkAccent200] = solveLeonardoAccent(darkPaper, darkLeoSeed, [7.2, 8.6]);

	// 强调实底与反白字：若用户种子在白字/浅纸上已满足 >=4.5:1 则原样保留，否则压暗至满足 4.5:1
	const lightOnEmphasis = lightPaper;
	const lightAccentEmphasis =
		wcagContrast(seedHex, lightOnEmphasis) >= 4.5
			? seedHex
			: solveLForContrast({
					bgHex: lightOnEmphasis,
					targetRatio: 4.6,
					H: seedOklch.H,
					C: Math.max(0.08, seedOklch.C),
					direction: "darker",
			  });

	const darkOnEmphasis = darkNeutral["900"];
	const darkAccentEmphasis = solveLForContrast({
		bgHex: darkOnEmphasis,
		targetRatio: 7.5,
		H: seedOklch.H,
		C: Math.min(0.12, Math.max(0.05, seedOklch.C * 0.85)),
		direction: "darker",
	});

	// 4. 异色 / 扩展语义状态色（默认包含 danger, success, warning, info）
	const statusSpecs = [
		{ key: "danger", preferredHue: 25, chroma: 0.19, always: true },
		{ key: "success", preferredHue: 148, chroma: 0.15, always: false },
		{ key: "warning", preferredHue: 68, chroma: 0.16, always: false },
		{ key: "info", preferredHue: 245, chroma: 0.16, always: false },
	];

	const statusLight = {};
	const statusDark = {};
	const hueConflicts = [];

	for (const spec of statusSpecs) {
		if (!spec.always && !withSemantic) continue;
		const dist = hueDistance(spec.preferredHue, seedOklch.H);
		const finalHue = spec.key === "danger" ? spec.preferredHue : pickSeparatedHue(spec.preferredHue, seedOklch.H, 35);
		if (spec.key === "danger" && dist < 45) {
			hueConflicts.push(`主品牌色（H=${seedOklch.H.toFixed(0)}°）与危险色（H=${finalHue}°）色相接近，请务必搭配错误图标或文字使用。`);
		}

		statusLight[spec.key] = {
			fg: solveLForContrast({ bgHex: lightPaper, targetRatio: 4.8, H: finalHue, C: spec.chroma, direction: "darker" }),
			muted: oklchToHex(0.945, Math.min(0.035, spec.chroma * 0.2), finalHue),
			emphasis: solveLForContrast({ bgHex: lightPaper, targetRatio: 4.6, H: finalHue, C: spec.chroma, direction: "darker" }),
			hue: Number(finalHue.toFixed(1)),
		};

		statusDark[spec.key] = {
			fg: solveLForContrast({ bgHex: darkPaper, targetRatio: 7.2, H: finalHue, C: spec.chroma * 0.9, direction: "lighter" }),
			muted: oklchToHex(0.24, Math.min(0.04, spec.chroma * 0.25), finalHue),
			emphasis: solveLForContrast({ bgHex: darkNeutral["900"], targetRatio: 6.5, H: finalHue, C: spec.chroma * 0.8, direction: "darker" }),
			hue: Number(finalHue.toFixed(1)),
		};
	}

	// 5. 组装 DTCG 基色层（color.primitives.tokens.json）
	const primitives = {
		$description: `基色层（DTCG）。由种子色 ${seedHex}（OKLCH H=${seedOklch.H.toFixed(1)}°, C=${seedOklch.C.toFixed(3)}, L=${seedOklch.L.toFixed(3)}）通过 OKLCH 中性阶反解 + Adobe Leonardo 强调阶求解生成。`,
		color: {
			$type: "color",
			light: {
				neutral: Object.fromEntries(
					Object.entries(lightNeutral).map(([step, val]) => [
						step,
						{
							$value: val,
							$description: step === "0" ? "亮色纸面" : `中性阶 ${step}（对纸 ${wcagContrast(val, lightPaper).toFixed(2)}:1）`,
							$extensions: { "com.color-system.solver": { source: "oklch-solver", hue: neutralCfg.hue } },
						},
					]),
				),
				accent: {
					"100": {
						$value: lightAccent100,
						$description: `强调前景（对纸 ${wcagContrast(lightAccent100, lightPaper).toFixed(2)}:1）`,
						$extensions: { "com.color-system.solver": { source: "leonardo", target: 4.85, seed: lightLeoSeed, background: lightPaper } },
					},
					"200": {
						$value: lightAccent200,
						$description: `强调 Hover（对纸 ${wcagContrast(lightAccent200, lightPaper).toFixed(2)}:1）`,
						$extensions: { "com.color-system.solver": { source: "leonardo", target: 5.85, seed: lightLeoSeed, background: lightPaper } },
					},
					emphasis: {
						$value: lightAccentEmphasis,
						$description: "强调实底（Banner / 主按钮 / 刊头）",
					},
				},
				surface: {
					deep: { $value: lightDeep, $description: "深图版固定底" },
					onDeep: { $value: lightPaper, $description: "深图版上的亮字" },
				},
				...Object.fromEntries(
					Object.entries(statusLight).map(([k, v]) => [
						k,
						{
							fg: { $value: v.fg, $description: `${k} 语义文字（对纸 ${wcagContrast(v.fg, lightPaper).toFixed(2)}:1）` },
							muted: { $value: v.muted, $description: `${k} 浅色提示底` },
							emphasis: { $value: v.emphasis, $description: `${k} 实底` },
						},
					]),
				),
			},
			dark: {
				neutral: Object.fromEntries(
					Object.entries(darkNeutral).map(([step, val]) => [
						step,
						{
							$value: val,
							$description: step === "0" ? "暗色纸面" : `暗色中性阶 ${step}（对纸 ${wcagContrast(val, darkPaper).toFixed(2)}:1）`,
							$extensions: { "com.color-system.solver": { source: "oklch-solver", hue: neutralCfg.hue } },
						},
					]),
				),
				accent: {
					"100": {
						$value: darkAccent100,
						$description: `暗色强调前景（对纸 ${wcagContrast(darkAccent100, darkPaper).toFixed(2)}:1）`,
						$extensions: { "com.color-system.solver": { source: "leonardo", target: 4.85, seed: darkLeoSeed, background: darkPaper } },
					},
					"200": {
						$value: darkAccent200,
						$description: `暗色强调 Hover（对纸 ${wcagContrast(darkAccent200, darkPaper).toFixed(2)}:1）`,
						$extensions: { "com.color-system.solver": { source: "leonardo", target: 5.85, seed: darkLeoSeed, background: darkPaper } },
					},
					emphasis: {
						$value: darkAccentEmphasis,
						$description: "暗色强调实底",
					},
				},
				surface: {
					deep: { $value: darkDeep, $description: "暗色深图版固定底" },
					onDeep: { $value: darkNeutral["900"], $description: "深图版上的亮字" },
				},
				...Object.fromEntries(
					Object.entries(statusDark).map(([k, v]) => [
						k,
						{
							fg: { $value: v.fg, $description: `暗色 ${k} 语义文字（对纸 ${wcagContrast(v.fg, darkPaper).toFixed(2)}:1）` },
							muted: { $value: v.muted, $description: `暗色 ${k} 浅色提示底` },
							emphasis: { $value: v.emphasis, $description: `暗色 ${k} 实底` },
						},
					]),
				),
			},
		},
	};

	// 6. 组装 DTCG 语义层（Primer 17 核心角色 + 可选扩展状态色，亮暗路径完全一致）
	function buildSemanticLayer(themeKey) {
		const base = {
			$type: "color",
			fgColor: {
				default: { $value: `{color.${themeKey}.neutral.900}`, $description: "主正文与标题" },
				muted: { $value: `{color.${themeKey}.neutral.400}`, $description: "次要说明、时间、元数据" },
				disabled: { $value: `{color.${themeKey}.neutral.300}`, $description: "禁用态文字与图标" },
				accent: { $value: `{color.${themeKey}.accent.100}`, $description: "链接与可交互强调文字" },
				accentHover: { $value: `{color.${themeKey}.accent.200}`, $description: "强调态 Hover / Pressed" },
				onEmphasis: { $value: themeKey === "light" ? `{color.${themeKey}.neutral.0}` : `{color.${themeKey}.neutral.900}`, $description: "强调实底上的反白文字" },
				onDeep: { $value: `{color.${themeKey}.surface.onDeep}`, $description: "深图版上的文字" },
				danger: { $value: `{color.${themeKey}.danger.fg}`, $description: "错误与危险操作文字" },
			},
			bgColor: {
				default: { $value: `{color.${themeKey}.neutral.0}`, $description: "页面与主内容底" },
				muted: { $value: `{color.${themeKey}.neutral.100}`, $description: "次级面板、表头、卡片衬底" },
				accent: {
					emphasis: { $value: `{color.${themeKey}.accent.emphasis}`, $description: "主按钮、刊头、整块强调平涂" },
				},
				deep: { $value: `{color.${themeKey}.surface.deep}`, $description: "深图版背景（亮暗皆深）" },
			},
			borderColor: {
				default: { $value: `{color.${themeKey}.neutral.300}`, $description: "输入框与交互控件边框" },
				muted: { $value: `{color.${themeKey}.neutral.200}`, $description: "分割线、发丝线" },
				emphasis: { $value: `{color.${themeKey}.neutral.900}`, $description: "强结构边界" },
				accent: { $value: `{color.${themeKey}.accent.100}`, $description: "选中态边框" },
			},
			focus: {
				outlineColor: { $value: `{color.${themeKey}.accent.100}`, $description: "键盘焦点环" },
			},
		};

		if (withSemantic) {
			for (const k of ["success", "warning", "info"]) {
				base.fgColor[k] = { $value: `{color.${themeKey}.${k}.fg}`, $description: `${k} 语义文字` };
				base.bgColor[k] = {
					muted: { $value: `{color.${themeKey}.${k}.muted}`, $description: `${k} 浅色提示底` },
					emphasis: { $value: `{color.${themeKey}.${k}.emphasis}`, $description: `${k} 实底` },
				};
			}
			base.bgColor.danger = {
				muted: { $value: `{color.${themeKey}.danger.muted}`, $description: "危险浅色提示底" },
				emphasis: { $value: `{color.${themeKey}.danger.emphasis}`, $description: "危险实底" },
			};
		}

		return base;
	}

	const lightSemantic = buildSemanticLayer("light");
	const darkSemantic = buildSemanticLayer("dark");

	// 7. 扁平化实际颜色值供 CSS / Tailwind / HTML 报告使用
	const flatLight = {
		"fgColor-default": lightNeutral["900"],
		"fgColor-muted": lightNeutral["400"],
		"fgColor-disabled": lightNeutral["300"],
		"fgColor-accent": lightAccent100,
		"fgColor-accentHover": lightAccent200,
		"fgColor-onEmphasis": lightOnEmphasis,
		"fgColor-onDeep": lightPaper,
		"fgColor-danger": statusLight.danger.fg,
		"bgColor-default": lightPaper,
		"bgColor-muted": lightNeutral["100"],
		"bgColor-accent-emphasis": lightAccentEmphasis,
		"bgColor-deep": lightDeep,
		"borderColor-default": lightNeutral["300"],
		"borderColor-muted": lightNeutral["200"],
		"borderColor-emphasis": lightNeutral["900"],
		"borderColor-accent": lightAccent100,
		"focus-outlineColor": lightAccent100,
	};

	const flatDark = {
		"fgColor-default": darkNeutral["900"],
		"fgColor-muted": darkNeutral["400"],
		"fgColor-disabled": darkNeutral["300"],
		"fgColor-accent": darkAccent100,
		"fgColor-accentHover": darkAccent200,
		"fgColor-onEmphasis": darkOnEmphasis,
		"fgColor-onDeep": darkNeutral["900"],
		"fgColor-danger": statusDark.danger.fg,
		"bgColor-default": darkPaper,
		"bgColor-muted": darkNeutral["100"],
		"bgColor-accent-emphasis": darkAccentEmphasis,
		"bgColor-deep": darkDeep,
		"borderColor-default": darkNeutral["300"],
		"borderColor-muted": darkNeutral["200"],
		"borderColor-emphasis": darkNeutral["900"],
		"borderColor-accent": darkAccent100,
		"focus-outlineColor": darkAccent100,
	};

	if (withSemantic) {
		for (const k of ["danger", "success", "warning", "info"]) {
			if (k !== "danger") {
				flatLight[`fgColor-${k}`] = statusLight[k].fg;
				flatDark[`fgColor-${k}`] = statusDark[k].fg;
			}
			flatLight[`bgColor-${k}-muted`] = statusLight[k].muted;
			flatLight[`bgColor-${k}-emphasis`] = statusLight[k].emphasis;
			flatDark[`bgColor-${k}-muted`] = statusDark[k].muted;
			flatDark[`bgColor-${k}-emphasis`] = statusDark[k].emphasis;
		}
	}

	// 8. 计算关键配对的双重对比度指标 (WCAG 2.1 + APCA Lc)
	function computePairMetrics(themeFlat) {
		const pairs = [
			{ fg: "fgColor-default", bg: "bgColor-default", label: "主正文 / 主背景", wcagMin: 7.0, apcaMin: 75 },
			{ fg: "fgColor-muted", bg: "bgColor-default", label: "次要文字 / 主背景", wcagMin: 4.5, apcaMin: 60 },
			{ fg: "fgColor-accent", bg: "bgColor-default", label: "强调文字 / 主背景", wcagMin: 4.5, apcaMin: 60 },
			{ fg: "fgColor-accentHover", bg: "bgColor-default", label: "强调Hover / 主背景", wcagMin: 4.5, apcaMin: 60 },
			{ fg: "fgColor-onEmphasis", bg: "bgColor-accent-emphasis", label: "反白字 / 强调实底", wcagMin: 4.5, apcaMin: 60 },
			{ fg: "fgColor-onDeep", bg: "bgColor-deep", label: "深图版字 / 深图版底", wcagMin: 7.0, apcaMin: 75 },
			{ fg: "fgColor-danger", bg: "bgColor-default", label: "危险文字 / 主背景", wcagMin: 4.5, apcaMin: 60 },
			{ fg: "borderColor-default", bg: "bgColor-default", label: "控件边框 / 主背景", wcagMin: 3.0, apcaMin: 30 },
			{ fg: "focus-outlineColor", bg: "bgColor-default", label: "焦点环 / 主背景", wcagMin: 3.0, apcaMin: 30 },
		];
		if (withSemantic) {
			for (const k of ["success", "warning", "info"]) {
				pairs.push({ fg: `fgColor-${k}`, bg: "bgColor-default", label: `${k}文字 / 主背景`, wcagMin: 4.5, apcaMin: 60 });
			}
		}
		return pairs.map((p) => {
			const fgHex = themeFlat[p.fg];
			const bgHex = themeFlat[p.bg];
			const wcag = Number(wcagContrast(fgHex, bgHex).toFixed(2));
			const lc = apcaContrast(fgHex, bgHex);
			return {
				...p,
				fgHex,
				bgHex,
				wcag,
				lc,
				passWcag: wcag >= p.wcagMin,
				passApca: Math.abs(lc) >= p.apcaMin,
			};
		});
	}

	return {
		meta: {
			seed: seedHex,
			slug,
			tint,
			withSemantic,
			seedOklch: {
				L: Number(seedOklch.L.toFixed(3)),
				C: Number(seedOklch.C.toFixed(3)),
				H: Number(seedOklch.H.toFixed(1)),
			},
			hueConflicts,
			generatedAt: new Date().toISOString(),
		},
		primitives,
		lightSemantic,
		darkSemantic,
		flatLight,
		flatDark,
		metrics: {
			light: computePairMetrics(flatLight),
			dark: computePairMetrics(flatDark),
		},
	};
}

/**
 * 渲染纯 CSS 变量输出
 */
function renderCssVariables(data) {
	const lightLines = Object.entries(data.flatLight).map(([k, v]) => `  --${k}: ${v};`);
	const darkLines = Object.entries(data.flatDark).map(([k, v]) => `  --${k}: ${v};`);
	return `/* ============================================================
   自动生成，请勿手改 | Seed: ${data.meta.seed}
   标准：Primer 语义角色 + Adobe Leonardo + OKLCH + W3C DTCG
   ============================================================ */

:root {
${lightLines.join("\n")}
}

.dark {
${darkLines.join("\n")}
}
`;
}

/**
 * 渲染 Tailwind CSS v4 @theme 扩展
 */
function renderTailwindV4(data) {
	const themeMappings = Object.keys(data.flatLight).map(
		(k) => `  --color-${k}: var(--${k});`,
	);
	return `/* ============================================================
   Tailwind CSS v4 @theme 色彩扩展 | Seed: ${data.meta.seed}
   用法：在全局 CSS 中 @import "./tokens.css"; @import "./tailwind.theme.css";
   即可直接使用 bg-bgColor-default, text-fgColor-accent, border-borderColor-default 等工具类
   ============================================================ */

@theme {
${themeMappings.join("\n")}
}
`;
}

/**
 * 渲染 Tailwind CSS v3 兼容 Preset
 */
function renderTailwindV3Preset(data) {
	const colors = {};
	for (const k of Object.keys(data.flatLight)) {
		colors[k] = `var(--${k})`;
	}
	return `/** @type {import('tailwindcss').Config} */
// Tailwind CSS v3 Preset | Seed: ${data.meta.seed}
module.exports = {
  theme: {
    extend: {
      colors: ${JSON.stringify(colors, null, 8).replace(/\n}$/, "\n      }")}
    }
  }
};
`;
}

// CLI 执行入口
const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
	const args = parseArgs(process.argv.slice(2));
	if (!args.seed) {
		console.error("✗ 请提供基础种子色，例如：pnpm generate -- --seed \"#007275\"");
		printHelp();
		process.exit(1);
	}

	const result = generateColorSystem(args);
	fs.mkdirSync(args.out, { recursive: true });

	const tokensOut = path.join(args.out, "tokens");
	fs.mkdirSync(tokensOut, { recursive: true });

	fs.writeFileSync(path.join(tokensOut, "color.primitives.tokens.json"), JSON.stringify(result.primitives, null, 2) + "\n");
	fs.writeFileSync(path.join(tokensOut, "color.light.tokens.json"), JSON.stringify(result.lightSemantic, null, 2) + "\n");
	fs.writeFileSync(path.join(tokensOut, "color.dark.tokens.json"), JSON.stringify(result.darkSemantic, null, 2) + "\n");

	if (args.writeTokens) {
		const rootTokens = path.join(ROOT, "tokens");
		fs.mkdirSync(rootTokens, { recursive: true });
		fs.writeFileSync(path.join(rootTokens, "color.primitives.tokens.json"), JSON.stringify(result.primitives, null, 2) + "\n");
		fs.writeFileSync(path.join(rootTokens, "color.light.tokens.json"), JSON.stringify(result.lightSemantic, null, 2) + "\n");
		fs.writeFileSync(path.join(rootTokens, "color.dark.tokens.json"), JSON.stringify(result.darkSemantic, null, 2) + "\n");
	}

	fs.writeFileSync(path.join(args.out, "tokens.css"), renderCssVariables(result));
	fs.writeFileSync(path.join(args.out, "tailwind.theme.css"), renderTailwindV4(result));
	fs.writeFileSync(path.join(args.out, "tailwind.preset.cjs"), renderTailwindV3Preset(result));

	const html = renderHtmlReport(result);
	fs.writeFileSync(path.join(args.out, "color-report.html"), html);

	console.log(`✓ 已根据种子色 ${result.meta.seed} 生成全套配色方案：`);
	console.log(`  - 人类可读报告: ${path.relative(ROOT, path.join(args.out, "color-report.html"))}`);
	console.log(`  - CSS 自定义变量: ${path.relative(ROOT, path.join(args.out, "tokens.css"))}`);
	console.log(`  - Tailwind v4 @theme: ${path.relative(ROOT, path.join(args.out, "tailwind.theme.css"))}`);
	console.log(`  - Tailwind v3 preset: ${path.relative(ROOT, path.join(args.out, "tailwind.preset.cjs"))}`);
	console.log(`  - W3C DTCG Tokens: ${path.relative(ROOT, tokensOut)}/`);
	if (result.meta.hueConflicts.length > 0) {
		for (const warn of result.meta.hueConflicts) console.log(`  ! 提示: ${warn}`);
	}
}
