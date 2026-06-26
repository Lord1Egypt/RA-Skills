"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.PinmuxAuditor = void 0;
const promises_1 = require("node:fs/promises");
const path_1 = __importDefault(require("path"));
const fs_1 = require("../common/fs");
class PinmuxAuditor {
    constructor() {
        this.rules = null;
        this.maxAuditPin = 64;
        this.chipAliasRules = [
            { pattern: /^esp32s3pico1/, target: 'esp32s3' },
            { pattern: /^esp32s3/, target: 'esp32s3' },
            { pattern: /^esp32c6/, target: 'esp32c6' },
            { pattern: /^esp32c5/, target: 'esp32c5' },
            { pattern: /^esp32c3/, target: 'esp32c3' },
            { pattern: /^esp32h2/, target: 'esp32h2' },
            { pattern: /^esp32p4/, target: 'esp32p4' },
            { pattern: /^esp32$/, target: 'esp32' }
        ];
    }
    resolveChipTarget(target = 'esp32') {
        const normalized = target.toLowerCase().replace(/[^a-z0-9]/g, '');
        for (const rule of this.chipAliasRules) {
            if (rule.pattern.test(normalized)) {
                return rule.target;
            }
        }
        return normalized || 'esp32';
    }
    /**
     * 加载对应芯片的物理规则库
     */
    async loadSocRules(target = 'esp32') {
        const resolvedTarget = this.resolveChipTarget(target);
        const candidates = [
            path_1.default.join(__dirname, `../data/soc/${resolvedTarget}.json`),
            path_1.default.join(process.cwd(), `src/data/soc/${resolvedTarget}.json`),
            path_1.default.join(process.cwd(), `dist/data/soc/${resolvedTarget}.json`)
        ];
        for (const rulePath of candidates) {
            if (await (0, fs_1.pathExists)(rulePath)) {
                this.rules = await (0, fs_1.readJsonFile)(rulePath);
                return;
            }
        }
        throw new Error(`未找到芯片 ${target} 的物理规则库（已归一化为 ${resolvedTarget}）`);
    }
    /**
     * 核心审计函数：对源码进行静态扫描
     */
    async auditSourceCode(projectPath) {
        if (!this.rules)
            throw new Error("规则库未加载");
        const sourceRoots = [path_1.default.join(projectPath, 'main'), path_1.default.join(projectPath, 'components')];
        const existingRoots = [];
        for (const root of sourceRoots) {
            if (await (0, fs_1.pathExists)(root)) {
                existingRoots.push(root);
            }
        }
        if (existingRoots.length === 0) {
            return [{
                    level: 'INFO',
                    message: "未找到 main/ 或 components/ 目录，已跳过 GPIO 静态审计。",
                    suggestion: "请确认 projectPath 指向 ESP-IDF 工程根目录。"
                }];
        }
        // 1. 获取所有 C/CPP 源码内容
        const sourceFiles = [];
        for (const root of existingRoots) {
            sourceFiles.push(...await this.getFiles(root, /\.(c|cpp|h)$/));
        }
        if (sourceFiles.length === 0) {
            return [{
                    level: 'INFO',
                    message: "在源码目录中未发现可审计的 C/C++ 文件。",
                    suggestion: "请确认工程源码已经生成，或补充 main/ 下的源文件。"
                }];
        }
        const sources = [];
        let combinedCode = "";
        for (const file of sourceFiles) {
            const content = await (0, promises_1.readFile)(file, 'utf-8');
            combinedCode += `${content}\n`;
            sources.push({
                path: file,
                relativePath: path_1.default.relative(projectPath, file),
                content,
                lines: content.split(/\r?\n/)
            });
        }
        // 2. 提取代码中引用的所有 GPIO 编号
        const symbols = this.buildSymbolTable(sources);
        const occurrences = this.collectPinOccurrences(sources, symbols);
        // 3. 执行规则审计
        const results = [];
        results.push(...this.checkFlashPins(occurrences));
        results.push(...this.checkInputOnlyPins(sources, occurrences));
        results.push(...this.checkStrappingPins(occurrences));
        results.push(...this.checkAdc2WifiConflict(sources, combinedCode, occurrences));
        return this.dedupeResults(results);
    }
    /**
     * 规则 1：拦截对内部 Flash/PSRAM 引脚的操作 (FATAL)
     */
    checkFlashPins(occurrences) {
        const results = [];
        const flashPins = this.rules.physical_limits.internal_flash_psram.pins;
        for (const pin of flashPins) {
            const occurrence = this.findFirstOccurrence(occurrences, pin);
            if (!occurrence)
                continue;
            results.push({
                level: 'FATAL',
                pin,
                file: occurrence.file,
                line: occurrence.line,
                evidence: occurrence.evidence,
                message: `检测到使用了 Flash/PSRAM 保留引脚 GPIO ${pin}。`,
                suggestion: "这些引脚通常连接内部存储或保留给 SPI0/1。请更换为普通 GPIO，避免启动失败或系统崩溃。"
            });
        }
        return results;
    }
    /**
     * 规则 2：检查 Input-Only 引脚是否被误设为输出 (ERROR)
     */
    checkInputOnlyPins(sources, occurrences) {
        const results = [];
        const inputOnly = this.rules.physical_limits.input_only_pins.pins;
        for (const pin of inputOnly) {
            const pinOccurrences = occurrences.filter((occurrence) => occurrence.pin === pin);
            for (const occurrence of pinOccurrences) {
                const source = sources.find((item) => item.relativePath === occurrence.file);
                if (!source || !this.isOutputContext(source, occurrence.line)) {
                    continue;
                }
                results.push({
                    level: 'CRITICAL',
                    pin,
                    file: occurrence.file,
                    line: occurrence.line,
                    evidence: occurrence.evidence,
                    message: `GPIO ${pin} 物理上仅支持输入，但代码中尝试设为输出。`,
                    suggestion: "该引脚缺少输出驱动电路，请更换为支持输出能力的 GPIO。"
                });
                break;
            }
        }
        return results;
    }
    /**
     * 规则 3：Strapping 引脚风险评估 (WARNING)
     */
    checkStrappingPins(occurrences) {
        const results = [];
        const strapData = this.rules.physical_limits.strapping_pins;
        for (const pin of strapData.pins) {
            const occurrence = this.findFirstOccurrence(occurrences, pin);
            if (!occurrence)
                continue;
            results.push({
                level: 'WARNING',
                pin,
                file: occurrence.file,
                line: occurrence.line,
                evidence: occurrence.evidence,
                message: `GPIO ${pin} 是启动配置(Strapping)引脚。`,
                suggestion: `注意：${strapData.critical_logic[pin.toString()] || '该引脚在上电/复位期间会影响启动行为。'} 建议在硬件电路上避免强拉高/低。`
            });
        }
        return results;
    }
    /**
     * 规则 4：ADC2 与 Wi-Fi 冲突审计 (CRITICAL)
     */
    checkAdc2WifiConflict(sources, code, occurrences) {
        const results = [];
        const isWifiUsed = code.includes("esp_wifi_start") || code.includes("esp_wifi_init");
        const isAdc2Used = code.includes("adc2_get_raw")
            || (code.includes("ADC_UNIT_2") && code.includes("adc"));
        const adc2Pins = this.rules.peripherals.adc.adc2;
        if (!isWifiUsed || !isAdc2Used) {
            return results;
        }
        for (const pin of adc2Pins) {
            const occurrence = this.findFirstOccurrence(occurrences.filter((item) => {
                if (item.pin !== pin)
                    return false;
                const source = sources.find((entry) => entry.relativePath === item.file);
                return source ? this.isAdcContext(source, item.line) : true;
            }), pin);
            if (!occurrence)
                continue;
            results.push({
                level: 'CRITICAL',
                pin,
                file: occurrence.file,
                line: occurrence.line,
                evidence: occurrence.evidence,
                message: "Wi-Fi 与 ADC2 存在硬件资源冲突。",
                suggestion: "Wi-Fi 开启时 ADC2 读数可能失败或不稳定。请将模拟采样引脚更换至 ADC1 域，或在关闭 Wi-Fi 的时段读取 ADC2。"
            });
        }
        return results;
    }
    /**
     * 工具函数：从源码中提取更丰富的 GPIO 引用方式
     */
    collectPinOccurrences(sources, symbols) {
        const occurrences = [];
        const seen = new Set();
        for (const source of sources) {
            source.lines.forEach((line, index) => {
                const pins = this.extractPinsFromLine(line, symbols);
                for (const pin of pins) {
                    const key = `${source.relativePath}:${index + 1}:${pin}`;
                    if (seen.has(key))
                        continue;
                    seen.add(key);
                    occurrences.push({
                        pin,
                        file: source.relativePath,
                        line: index + 1,
                        evidence: line.trim().slice(0, 200),
                        isDefinition: this.isSymbolDefinitionLine(line)
                    });
                }
            });
        }
        return occurrences;
    }
    buildSymbolTable(sources) {
        const symbols = new Map();
        for (let pass = 0; pass < 4; pass += 1) {
            let changed = false;
            for (const source of sources) {
                source.lines.forEach((line, index) => {
                    const definitions = this.extractSymbolDefinitions(line, symbols);
                    for (const definition of definitions) {
                        const existing = symbols.get(definition.name);
                        if (existing?.pin === definition.pin) {
                            continue;
                        }
                        symbols.set(definition.name, {
                            pin: definition.pin,
                            file: source.relativePath,
                            line: index + 1
                        });
                        changed = true;
                    }
                });
            }
            if (!changed) {
                break;
            }
        }
        return symbols;
    }
    extractPinsFromLine(line, symbols) {
        const pins = new Set();
        const patterns = [
            /GPIO_NUM_(\d+)/g,
            /GPIO_SEL_(\d+)/g,
            /(?:gpio_(?:set_level|set_direction|reset_pin|set_pull_mode|set_intr_type|set_drive_capability|hold_en|hold_dis|pullup_en|pullup_dis|pulldown_en|pulldown_dis))\s*\(\s*(\d+)/g,
            /(?:\.|\b)(?:gpio_num|pin|pins|sda_io_num|scl_io_num|mosi_io_num|miso_io_num|clk_io_num|cs_io_num|tx_io_num|rx_io_num|rts_io_num|cts_io_num|dc_gpio_num|reset_gpio_num|int_gpio_num|irq_gpio_num|busy_gpio_num|wp_gpio_num|hd_gpio_num|quadwp_io_num|quadhd_io_num)\s*=\s*(-?\d+)/g,
            /pin_bit_mask\s*=\s*(?:1ULL|1UL|1U|1)\s*<<\s*(\d+)/g,
            /pin_bit_mask\s*=\s*BIT(?:64)?\(\s*(\d+)\s*\)/g
        ];
        for (const pattern of patterns) {
            const matches = line.matchAll(pattern);
            for (const match of matches) {
                const pin = Number.parseInt(match[1], 10);
                if (Number.isNaN(pin) || pin < 0 || pin > this.maxAuditPin) {
                    continue;
                }
                pins.add(pin);
            }
        }
        const symbolicPatterns = [
            /(?:gpio_(?:set_level|set_direction|reset_pin|set_pull_mode|set_intr_type|set_drive_capability|hold_en|hold_dis|pullup_en|pullup_dis|pulldown_en|pulldown_dis))\s*\(\s*([A-Za-z_]\w*)/g,
            /(?:\.|\b)(?:gpio_num|pin|pins|sda_io_num|scl_io_num|mosi_io_num|miso_io_num|clk_io_num|cs_io_num|tx_io_num|rx_io_num|rts_io_num|cts_io_num|dc_gpio_num|reset_gpio_num|int_gpio_num|irq_gpio_num|busy_gpio_num|wp_gpio_num|hd_gpio_num|quadwp_io_num|quadhd_io_num)\s*=\s*([A-Za-z_]\w*)/g,
            /pin_bit_mask\s*=\s*([A-Za-z_]\w+)/g,
            /pin_bit_mask\s*=\s*(?:1ULL|1UL|1U|1)\s*<<\s*([A-Za-z_]\w+)/g,
            /pin_bit_mask\s*=\s*BIT(?:64)?\(\s*([A-Za-z_]\w+)\s*\)/g
        ];
        for (const pattern of symbolicPatterns) {
            const matches = line.matchAll(pattern);
            for (const match of matches) {
                const resolved = this.resolvePinExpression(match[1], symbols);
                if (resolved !== null) {
                    pins.add(resolved);
                }
            }
        }
        return [...pins];
    }
    extractSymbolDefinitions(line, symbols) {
        const definitions = [];
        const patterns = [
            /^#define\s+([A-Za-z_]\w*)\s+(.+)$/,
            /\b(?:static\s+)?(?:constexpr\s+)?(?:const\s+)?(?:gpio_num_t|int|unsigned|uint8_t|uint16_t|uint32_t|int32_t|size_t)\s+([A-Za-z_]\w*)\s*=\s*([^;]+);/
        ];
        for (const pattern of patterns) {
            const match = line.match(pattern);
            if (!match)
                continue;
            const name = match[1];
            const pin = this.resolvePinExpression(match[2], symbols);
            if (pin === null)
                continue;
            definitions.push({ name, pin });
        }
        const assignmentMatch = line.match(/^\s*([A-Za-z_]\w*)\s*=\s*([^;]+);/);
        if (assignmentMatch) {
            const name = assignmentMatch[1];
            const pin = this.resolvePinExpression(assignmentMatch[2], symbols);
            if (pin !== null && (symbols.has(name) || this.looksLikePinRelatedIdentifier(name))) {
                definitions.push({ name, pin });
            }
        }
        return definitions;
    }
    isSymbolDefinitionLine(line) {
        return /^#define\s+([A-Za-z_]\w*)\s+(.+)$/.test(line)
            || /\b(?:static\s+)?(?:constexpr\s+)?(?:const\s+)?(?:gpio_num_t|int|unsigned|uint8_t|uint16_t|uint32_t|int32_t|size_t)\s+([A-Za-z_]\w*)\s*=\s*([^;]+);/.test(line)
            || /^\s*([A-Za-z_]\w*)\s*=\s*([^;]+);/.test(line);
    }
    resolvePinExpression(expression, symbols) {
        let value = expression.trim();
        if (!value) {
            return null;
        }
        value = value.replace(/\/\/.*$/, '').trim();
        value = value.replace(/\/\*.*?\*\//g, '').trim();
        while (value.startsWith('(') && value.endsWith(')')) {
            value = value.slice(1, -1).trim();
        }
        value = value.replace(/^[A-Za-z_]\w*\s*\)\s*/, '').trim();
        const gpioMatch = value.match(/^GPIO_NUM_(\d+)$/);
        if (gpioMatch) {
            return Number.parseInt(gpioMatch[1], 10);
        }
        const numericMatch = value.match(/^(?:0x([0-9a-fA-F]+)|(\d+))$/);
        if (numericMatch) {
            const parsed = numericMatch[1]
                ? Number.parseInt(numericMatch[1], 16)
                : Number.parseInt(numericMatch[2], 10);
            return parsed >= 0 && parsed <= this.maxAuditPin ? parsed : null;
        }
        const shiftMatch = value.match(/^(?:1ULL|1UL|1U|1)\s*<<\s*(.+)$/);
        if (shiftMatch) {
            return this.resolvePinExpression(shiftMatch[1], symbols);
        }
        const bitMatch = value.match(/^BIT(?:64)?\(\s*(.+?)\s*\)$/);
        if (bitMatch) {
            return this.resolvePinExpression(bitMatch[1], symbols);
        }
        const identifierMatch = value.match(/^([A-Za-z_]\w*)$/);
        if (identifierMatch) {
            return symbols.get(identifierMatch[1])?.pin ?? null;
        }
        return null;
    }
    looksLikePinRelatedIdentifier(name) {
        return /(gpio|pin|io|sda|scl|mosi|miso|clk|cs|tx|rx|rst|reset|irq|int|busy)/i.test(name);
    }
    isOutputContext(source, line) {
        const snippet = this.getSnippet(source, line, 3).join('\n');
        return /GPIO_MODE_OUTPUT|GPIO_MODE_OUTPUT_OD|GPIO_MODE_INPUT_OUTPUT|gpio_set_level|gpio_set_direction|gpio_reset_pin|gpio_hold_en|gpio_hold_dis/.test(snippet);
    }
    isAdcContext(source, line) {
        const snippet = this.getSnippet(source, line, 3).join('\n');
        return /\badc\b|adc2_get_raw|adc_oneshot|ADC_UNIT_2|adc_channel_t/i.test(snippet);
    }
    getSnippet(source, centerLine, radius) {
        const start = Math.max(0, centerLine - radius - 1);
        const end = Math.min(source.lines.length, centerLine + radius);
        return source.lines.slice(start, end);
    }
    findFirstOccurrence(occurrences, pin) {
        const matching = occurrences.filter((occurrence) => occurrence.pin === pin);
        return matching.find((occurrence) => !occurrence.isDefinition) || matching[0];
    }
    dedupeResults(results) {
        const seen = new Set();
        return results.filter((result) => {
            const key = [
                result.level,
                result.pin ?? '',
                result.file ?? '',
                result.line ?? '',
                result.message
            ].join('|');
            if (seen.has(key)) {
                return false;
            }
            seen.add(key);
            return true;
        });
    }
    async getFiles(dir, filter) {
        if (!await (0, fs_1.pathExists)(dir)) {
            return [];
        }
        const files = await (0, promises_1.readdir)(dir);
        let results = [];
        for (const file of files) {
            const fullPath = path_1.default.join(dir, file);
            if ((await (0, promises_1.stat)(fullPath)).isDirectory()) {
                results = results.concat(await this.getFiles(fullPath, filter));
            }
            else if (filter.test(file)) {
                results.push(fullPath);
            }
        }
        return results;
    }
}
exports.PinmuxAuditor = PinmuxAuditor;
//# sourceMappingURL=PinmuxAuditor.js.map