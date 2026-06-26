import { ensureRequired, parseCliArgs, safeJsonParse, writeJson, } from "../../shared/fs.js";
const PILLAR_PATTERN = /(?:\|\s*)?(年柱|月柱|日柱|时柱)\s*[:：|]\s*([甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥\w]+)/g;
const CITY_LONGITUDE = {
    北京: 116.40,
    上海: 121.47,
    广州: 113.26,
    深圳: 114.06,
    杭州: 120.16,
    南京: 118.80,
    成都: 104.06,
    重庆: 106.55,
    武汉: 114.31,
    西安: 108.94,
    天津: 117.20,
    苏州: 120.58,
    长沙: 112.94,
    郑州: 113.62,
    青岛: 120.38,
};
const STANDARD_MERIDIAN = 120;
export function normalizeDateInput(rawDate) {
    const value = rawDate.trim();
    const direct = value
        .replace(/\//g, "-")
        .replace(/年/g, "-")
        .replace(/月/g, "-")
        .replace(/日/g, "")
        .replace(/\s+/g, "")
        .replace(/--+/g, "-");
    const directMatch = /^(\d{2,4})-(\d{1,2})-(\d{1,2})$/.exec(direct);
    if (!directMatch) {
        throw new Error([
            "出生日期无法解析。",
            "你可以自然输入（如 1996年8月12日），我会自动转换；也可直接用 YYYY-MM-DD。",
            "示例：1993-10-21",
        ].join("\n"));
    }
    let year = Number.parseInt(directMatch[1], 10);
    if (directMatch[1].length === 2) {
        const nowYear = new Date().getFullYear() % 100;
        year += year <= nowYear ? 2000 : 1900;
    }
    const month = Number.parseInt(directMatch[2], 10);
    const day = Number.parseInt(directMatch[3], 10);
    return `${year.toString().padStart(4, "0")}-${month
        .toString()
        .padStart(2, "0")}-${day.toString().padStart(2, "0")}`;
}
export function validateDate(date) {
    const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(date);
    if (!match) {
        throw new Error([
            "出生日期格式不正确。",
            "请使用 YYYY-MM-DD，或自然输入如“1996年8月12日”。",
            "示例：1993-10-21",
        ].join("\n"));
    }
    const d = new Date(`${date}T00:00:00`);
    if (Number.isNaN(d.getTime())) {
        throw new Error([
            "出生日期无法识别。",
            "请确认日期是真实存在的公历日期。",
            "示例：1993-10-21",
        ].join("\n"));
    }
}
export function validateTime(time) {
    const match = /^([01]\d|2[0-3]):([0-5]\d)$/.exec(time);
    if (!match) {
        throw new Error([
            "出生时间格式不正确。",
            "支持自然表达（如 下午3点半 / 3:30pm），也支持 24 小时制 HH:mm。",
            "示例：09:30、21:45、下午3点半",
        ].join("\n"));
    }
}
export function normalizeTimeInput(rawTime) {
    const value = rawTime.trim().toLowerCase();
    if (!value) {
        return value;
    }
    const markerMatch = /(上午|中午|下午|晚上|凌晨|am|pm)/.exec(value);
    const marker = markerMatch?.[0] ?? "";
    const replaced = value
        .replace(/：/g, ":")
        .replace(/点半/g, ":30")
        .replace(/点/g, ":00")
        .replace(/分/g, "")
        .replace(/\s+/g, "")
        .replace(/上午|中午|下午|晚上|凌晨|am|pm/g, "");
    const m = /^(\d{1,2})(?::(\d{1,2}))?/.exec(replaced);
    if (!m) {
        throw new Error([
            "出生时间无法解析。",
            "你可以自然输入（如 下午3点半），我会自动转换；也可直接用 HH:mm。",
            "示例：09:30 / 下午3点半",
        ].join("\n"));
    }
    let hour = Number.parseInt(m[1], 10);
    const minute = Number.parseInt(m[2] ?? "0", 10);
    if (marker === "pm" || marker === "下午" || marker === "晚上") {
        if (hour < 12) {
            hour += 12;
        }
    }
    else if (marker === "am" || marker === "凌晨" || marker === "上午") {
        if (hour === 12) {
            hour = 0;
        }
    }
    else if (marker === "中午") {
        if (hour < 11) {
            hour += 12;
        }
    }
    return `${hour.toString().padStart(2, "0")}:${minute
        .toString()
        .padStart(2, "0")}`;
}
function formatIso(date, time) {
    return `${date}T${time}:00`;
}
function normalizeLocationKey(location) {
    return location.replace(/[省市县区]/g, "").trim();
}
function resolveLongitude(location, manual) {
    if (Number.isFinite(manual)) {
        return manual;
    }
    const key = normalizeLocationKey(location);
    if (CITY_LONGITUDE[key] !== undefined) {
        return CITY_LONGITUDE[key];
    }
    const fuzzy = Object.keys(CITY_LONGITUDE).find((item) => key.includes(item));
    return fuzzy ? CITY_LONGITUDE[fuzzy] : undefined;
}
function applyDayRollover(date, time, dayRolloverHour) {
    const [hourStr] = time.split(":");
    const hour = Number.parseInt(hourStr, 10);
    if (!Number.isFinite(hour) || hour < dayRolloverHour) {
        return { date, time };
    }
    const d = new Date(`${date}T00:00:00`);
    d.setDate(d.getDate() + 1);
    const nextDate = `${d.getFullYear()}-${`${d.getMonth() + 1}`.padStart(2, "0")}-${`${d.getDate()}`.padStart(2, "0")}`;
    return { date: nextDate, time };
}
function applyTrueSolarTime(time, longitude) {
    if (!Number.isFinite(longitude)) {
        return { time };
    }
    const [h, m] = time.split(":").map((x) => Number.parseInt(x, 10));
    const baseMinutes = h * 60 + m;
    const correctionMinutes = Math.round((Number(longitude) - STANDARD_MERIDIAN) * 4);
    const shifted = baseMinutes + correctionMinutes;
    const wrapped = ((shifted % 1440) + 1440) % 1440;
    const nh = Math.floor(wrapped / 60);
    const nm = wrapped % 60;
    return {
        time: `${`${nh}`.padStart(2, "0")}:${`${nm}`.padStart(2, "0")}`,
        correctionMinutes,
    };
}
function normalizePillarValue(value) {
    if (!value) {
        return undefined;
    }
    if (typeof value === "string") {
        return value.trim();
    }
    if (typeof value === "object") {
        const record = value;
        const gan = toStringValue(record.gan ?? record.stem ?? record["天干"]);
        const zhi = toStringValue(record.zhi ?? record.branch ?? record["地支"]);
        if (gan || zhi) {
            return `${gan ?? ""}${zhi ?? ""}`.trim();
        }
    }
    return undefined;
}
function toStringValue(value) {
    if (typeof value === "string") {
        return value.trim();
    }
    if (typeof value === "number") {
        return `${value}`;
    }
    return undefined;
}
function deepFindByKeys(node, keyCandidates) {
    if (!node || typeof node !== "object") {
        return undefined;
    }
    const record = node;
    for (const key of Object.keys(record)) {
        if (keyCandidates.includes(key)) {
            return record[key];
        }
    }
    for (const child of Object.values(record)) {
        const found = deepFindByKeys(child, keyCandidates);
        if (found !== undefined) {
            return found;
        }
    }
    return undefined;
}
function parsePillarsFromMarkdown(markdown) {
    const pillars = {};
    PILLAR_PATTERN.lastIndex = 0;
    let match = PILLAR_PATTERN.exec(markdown);
    while (match) {
        const [, label, value] = match;
        if (label === "年柱") {
            pillars.year = value;
        }
        if (label === "月柱") {
            pillars.month = value;
        }
        if (label === "日柱") {
            pillars.day = value;
        }
        if (label === "时柱") {
            pillars.hour = value;
        }
        match = PILLAR_PATTERN.exec(markdown);
    }
    return pillars;
}
function parseDayMasterFromMarkdown(markdown) {
    const line = /(?:日主|日元)\s*[:：]\s*([甲乙丙丁戊己庚辛壬癸\w]+)/.exec(markdown) ??
        /\|\s*(?:日主|日元)\s*\|\s*([甲乙丙丁戊己庚辛壬癸\w]+)/.exec(markdown);
    return line?.[1];
}
function pruneHourSensitive(node) {
    if (Array.isArray(node)) {
        const mapped = node
            .map((item) => pruneHourSensitive(item))
            .filter((item) => item !== undefined);
        if (mapped.length === 4) {
            return mapped.slice(0, 3);
        }
        return mapped;
    }
    if (!node || typeof node !== "object") {
        if (typeof node === "string" && /(时柱|时支|时干|时宫)/.test(node)) {
            return undefined;
        }
        if (typeof node === "string" && /[子丑寅卯辰巳午未申酉戌亥]时/.test(node)) {
            return node.replace(/[甲乙丙丁戊己庚辛壬癸]?[子丑寅卯辰巳午未申酉戌亥]时/g, "").trim() || undefined;
        }
        if (typeof node === "string" &&
            /(刑|冲|合|会)/.test(node) &&
            /时/.test(node)) {
            return undefined;
        }
        return node;
    }
    const record = node;
    const next = {};
    for (const [key, value] of Object.entries(record)) {
        if (/(hour|shi|hourPillar|timePillar|时柱|时支|时干|时宫)/i.test(key)) {
            continue;
        }
        if (/(interaction|刑|冲|合|会)/i.test(key) && /时/.test(JSON.stringify(value))) {
            continue;
        }
        const pruned = pruneHourSensitive(value);
        if (pruned !== undefined) {
            next[key] = pruned;
        }
    }
    return next;
}
function stripHourLines(markdown) {
    let text = markdown;
    text = text.replace(/\n###\s*时柱[\s\S]*?(?=\n###|\n##|$)/g, "\n");
    text = text.replace(/\n##\s*刑冲合会[\s\S]*?(?=\n##|$)/g, "\n");
    const lines = text
        .split("\n")
        .map((line) => {
        if (/^\s*-\s*阳历：/.test(line)) {
            return line.replace(/(\d{4}年\d{1,2}月\d{1,2}日)\s+\d{1,2}:\d{2}:\d{2}/, "$1");
        }
        if (/^\s*-\s*农历：/.test(line)) {
            return "- 农历：（缺少出生时间，已省略时柱相关信息）";
        }
        if (/^\s*-\s*八字：/.test(line)) {
            const value = line.replace(/^\s*-\s*八字：\s*/, "");
            const pillars = value.split(/\s+/).filter(Boolean);
            if (pillars.length >= 4) {
                return `- 八字：${pillars.slice(0, 3).join(" ")}`;
            }
        }
        return line;
    })
        .filter((line) => !/(时柱|时支|时干|时宫)/.test(line))
        .filter((line) => !(/(刑|冲|合|会)/.test(line) && /时/.test(line)));
    return lines.join("\n").replace(/\n{3,}/g, "\n\n");
}
function sanitizeRawBaziForMissingTime(raw) {
    const pruned = pruneHourSensitive(raw);
    if (!pruned || typeof pruned !== "object" || Array.isArray(pruned)) {
        return pruned;
    }
    const record = { ...pruned };
    const solar = toStringValue(record["阳历"]);
    if (solar) {
        record["阳历"] = solar.replace(/\s+\d{1,2}:\d{2}:\d{2}/, "");
    }
    const lunar = toStringValue(record["农历"]);
    if (lunar) {
        record["农历"] = lunar
            .replace(/[甲乙丙丁戊己庚辛壬癸]?[子丑寅卯辰巳午未申酉戌亥]时/g, "")
            .replace(/\s+/g, " ")
            .trim();
    }
    const bazi = toStringValue(record["八字"]);
    if (bazi) {
        const pillars = bazi.split(/\s+/).filter(Boolean);
        if (pillars.length >= 4) {
            record["八字"] = pillars.slice(0, 3).join(" ");
        }
    }
    delete record["时柱"];
    return record;
}
function ensureStructuredPillars(raw, markdown) {
    const fromMarkdown = parsePillarsFromMarkdown(markdown);
    const yearFromRaw = normalizePillarValue(deepFindByKeys(raw, ["yearPillar", "year", "nianZhu", "年柱"]));
    const monthFromRaw = normalizePillarValue(deepFindByKeys(raw, ["monthPillar", "month", "yueZhu", "月柱"]));
    const dayFromRaw = normalizePillarValue(deepFindByKeys(raw, ["dayPillar", "day", "riZhu", "日柱"]));
    const hourFromRaw = normalizePillarValue(deepFindByKeys(raw, ["hourPillar", "hour", "shiZhu", "时柱"]));
    return {
        year: fromMarkdown.year ?? yearFromRaw,
        month: fromMarkdown.month ?? monthFromRaw,
        day: fromMarkdown.day ?? dayFromRaw,
        hour: fromMarkdown.hour ?? hourFromRaw,
    };
}
function normalizeFiveElements(raw) {
    return (deepFindByKeys(raw, ["fiveElements", "wuxing", "五行"]) ??
        "（暂未提取到结构化五行信息，可参考 raw_markdown）");
}
function normalizeTenGods(raw) {
    return (deepFindByKeys(raw, ["tenGods", "shiShen", "shishen", "十神"]) ??
        "（暂未提取到结构化十神信息，可参考 raw_markdown）");
}
function normalizeLuckCycles(raw) {
    return (deepFindByKeys(raw, ["daYun", "dayun", "luckCycles", "bigLuck", "大运"]) ??
        "（暂未提取到结构化大运信息，可参考 raw_markdown）");
}
function buildYearlyFortune(raw, pillars) {
    try {
        const baziRecord = raw;
        const baziStr = (baziRecord?.["八字"] ?? "").replaceAll(" ", "");
        if (!baziStr || baziStr.length < 8) {
            return "（八字信息不完整，无法计算流年）";
        }
        // Dynamic import would be async; we are in sync context here.
        // Build a structured summary from what we already have in raw.
        const year = new Date().getFullYear();
        const pillarArr = [pillars.year, pillars.month, pillars.day, pillars.hour].filter((p) => !!p);
        return {
            current_year: year,
            pillars: pillarArr,
            bazi: baziStr,
            note: "流年干支、神煞与刑冲合会由运行时 buildFlowSnapshotMarkdown 实时计算",
        };
    }
    catch {
        return "（流年信息计算失败，可参考 raw_markdown）";
    }
}
async function calcRawBazi(args) {
    let buildBaziFromSolar;
    let buildBaziFromLunar;
    let baziToMarkdown;
    try {
        const pkg = (await import("cantian-tymext"));
        buildBaziFromSolar = pkg.buildBaziFromSolar;
        buildBaziFromLunar = pkg.buildBaziFromLunar;
        baziToMarkdown = pkg.baziToMarkdown;
    }
    catch {
        throw new Error([
            "排盘依赖未就绪，当前无法完成八字计算。",
            "请先执行：npm install",
            "若仍失败，请确认 package.json 中 cantian-tymext 已成功安装。",
        ].join("\n"));
    }
    if (!buildBaziFromSolar || !buildBaziFromLunar || !baziToMarkdown) {
        throw new Error([
            "排盘模块加载失败。",
            "缺少 buildBaziFromSolar/buildBaziFromLunar/baziToMarkdown 导出。",
            "请确认 cantian-tymext 版本是否匹配。",
        ].join("\n"));
    }
    const mappedGender = args.gender === "male" ? 1 : 0;
    const raw = args.calendarType === "solar"
        ? buildBaziFromSolar({
            solarTime: args.isoTime,
            gender: mappedGender,
            sect: args.sect,
        })
        : buildBaziFromLunar({
            lunarTime: args.isoTime,
            gender: mappedGender,
            sect: args.sect,
        });
    const markdown = baziToMarkdown(raw);
    return { raw, markdown };
}
export async function buildChart(input) {
    validateDate(input.date);
    if (input.time) {
        validateTime(input.time);
    }
    const rawClockTime = input.time ?? "12:00";
    const dayRolloverHour = Number.isFinite(input.dayRolloverHour) ? Number(input.dayRolloverHour) : 23;
    const rolled = applyDayRollover(input.date, rawClockTime, dayRolloverHour);
    const longitude = resolveLongitude(input.location, input.longitude);
    const trueSolarMode = input.trueSolarMode ?? "auto";
    const shouldApplyTrueSolar = trueSolarMode === "on" || (trueSolarMode === "auto" && Number.isFinite(longitude));
    const trueSolarResult = shouldApplyTrueSolar
        ? applyTrueSolarTime(rolled.time, longitude)
        : { time: rolled.time };
    const effectiveDate = rolled.date;
    const effectiveTime = trueSolarResult.time;
    const accuracyMode = input.time
        ? "full_chart"
        : "missing_time_six_pillars";
    const rawResult = await calcRawBazi({
        calendarType: input.calendarType,
        isoTime: formatIso(effectiveDate, effectiveTime),
        gender: input.gender,
        sect: input.sect,
    });
    const pillars = ensureStructuredPillars(rawResult.raw, rawResult.markdown);
    const dayMaster = toStringValue(deepFindByKeys(rawResult.raw, [
        "dayMaster",
        "riGan",
        "dayStem",
        "日主",
        "日元",
    ])) ?? parseDayMasterFromMarkdown(rawResult.markdown);
    const chart = {
        schema_version: "1.0.0",
        generated_at: new Date().toISOString(),
        source_command: input.sourceCommand,
        accuracy_mode: accuracyMode,
        requires_birth_time_for_full_accuracy: !input.time,
        notes: [],
        birth_input: {
            name: input.name,
            date: effectiveDate,
            provided_time: input.time,
            clock_time: rawClockTime,
            true_solar_time: shouldApplyTrueSolar ? effectiveTime : undefined,
            time_correction_minutes: shouldApplyTrueSolar ? trueSolarResult.correctionMinutes : undefined,
            effective_time: effectiveTime,
            location: input.location,
            longitude,
            true_solar_mode: trueSolarMode,
            day_rollover_hour: dayRolloverHour,
            gender: input.gender,
            calendar_type: input.calendarType,
            sect: input.sect,
        },
        pillars,
        day_master: dayMaster,
        five_elements: normalizeFiveElements(rawResult.raw),
        ten_gods: normalizeTenGods(rawResult.raw),
        luck_cycles: normalizeLuckCycles(rawResult.raw),
        current_year: new Date().getFullYear(),
        yearly_fortune: buildYearlyFortune(rawResult.raw, pillars),
        removed_due_to_missing_time: [],
        raw_markdown: rawResult.markdown,
        raw_bazi: rawResult.raw,
    };
    if (!input.time) {
        chart.notes.push("未提供出生时间，已采用 12:00 进行内部计算，并按六柱精简模式输出。");
        chart.notes.push("补充出生时间后可重算为完整精度版本。");
        chart.removed_due_to_missing_time = [
            "时柱",
            "与时柱相关的刑冲合会",
            "时柱衍生关系",
        ];
        chart.pillars.hour = undefined;
        chart.raw_bazi = sanitizeRawBaziForMissingTime(chart.raw_bazi);
        chart.raw_markdown = stripHourLines(chart.raw_markdown);
        chart.five_elements = pruneHourSensitive(chart.five_elements);
        chart.ten_gods = pruneHourSensitive(chart.ten_gods);
        chart.luck_cycles = pruneHourSensitive(chart.luck_cycles);
        chart.yearly_fortune = pruneHourSensitive(chart.yearly_fortune);
    }
    return chart;
}
async function main() {
    const args = parseCliArgs(process.argv);
    ensureRequired(args, ["name", "location", "gender"]);
    const rawDate = args.date ?? args["birth-date"] ?? args.birth ?? "";
    if (!rawDate) {
        throw new Error([
            "缺少出生日期。",
            "请提供 date（支持自然格式）。",
            "示例：--date \"1996年8月12日\"",
        ].join("\n"));
    }
    const date = normalizeDateInput(rawDate);
    const time = args.time ? normalizeTimeInput(args.time) : undefined;
    validateDate(date);
    if (time) {
        validateTime(time);
    }
    const genderArg = args.gender.toLowerCase();
    const gender = genderArg === "male" || genderArg === "男"
        ? "male"
        : genderArg === "female" || genderArg === "女"
            ? "female"
            : (() => {
                throw new Error([
                    "性别参数无效。",
                    "请使用 male/female（或 男/女）。",
                    "示例：--gender male",
                ].join("\n"));
            })();
    const chart = await buildChart({
        name: args.name,
        date,
        time,
        location: args.location,
        gender,
        calendarType: args.calendar === "lunar" || args.calendar === "农历" ? "lunar" : "solar",
        sect: args.sect === "1" ? 1 : 2,
        sourceCommand: args.command === "/bazi-persona update"
            ? "/bazi-persona update"
            : "/bazi-persona create",
        trueSolarMode: args["true-solar"] === "on" || args["true-solar"] === "off"
            ? args["true-solar"]
            : "auto",
        longitude: args.longitude ? Number.parseFloat(args.longitude) : undefined,
        dayRolloverHour: args["day-rollover"] ? Number.parseInt(args["day-rollover"], 10) : 23,
    });
    const output = args.output;
    if (output) {
        writeJson(output, chart);
        process.stdout.write(`已生成 chart.json：${output}\n`);
        return;
    }
    process.stdout.write(`${JSON.stringify(chart, null, 2)}\n`);
}
if (import.meta.url === `file://${process.argv[1]}`) {
    main().catch((error) => {
        const fallback = safeJsonParse(JSON.stringify(error), {});
        const message = error instanceof Error
            ? error.message
            : fallback.message ?? "未知错误，请稍后重试。";
        process.stderr.write(`${message}\n`);
        process.exitCode = 1;
    });
}
