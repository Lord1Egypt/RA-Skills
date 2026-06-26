# Extraction Templates

Extraction templates for datasheet analysis. Each template defines the required structure and validation rules.

---

## Device Info Template

```json
{
    "_template": "device_info",
    "_version": "1.0",
    "manufacturer": "",
    "part_number": "",
    "full_part_number": "",
    "description": "",
    "category": "",
    "package": {
        "type": "",
        "pin_count": 0,
        "dimensions": ""
    },
    "temperature_range": {
        "operating": {"min": "", "max": ""},
        "storage": {"min": "", "max": ""}
    },
    "source": {
        "cover_page": 1,
        "pin_config_page": 0,
        "specs_page": 0
    }
}
```

**Validation Rules:**
- `package.pin_count` MUST match the number in `package.type`
- Example: `QFN-32` → `pin_count: 32`
- All source page numbers must be filled after extraction

---

## Power Domains Template

```json
{
    "_template": "power_domains",
    "_version": "1.0",
    "power_domains": [
        {
            "name": "",
            "pin_names": [],
            "min_voltage": "",
            "typ_voltage": "",
            "max_voltage": "",
            "current_typ": "",
            "purpose": "",
            "decoupling": ""
        }
    ],
    "ground_pins": [],
    "source_page": 0
}
```

**Extraction Rules:**
- MUST extract ALL power pins from Pin Description table
- NOT just examples - list all pins with pin numbers
- WRONG: `"VDD"`
- CORRECT: `"VDD (pins 1, 13, 32, 48)"`
- Check for special power domains: CPVDD, HPVDD, PLLVDD, etc.

---

## I2C Interface Template

```json
{
    "_template": "i2c_interface",
    "_version": "1.0",
    "interface_type": "I2C",
    "pins": {
        "scl": "",
        "sda": ""
    },
    "address": {
        "format_shown": "",
        "format_explanation": "",
        "address_7bit": [],
        "address_8bit_write": [],
        "address_8bit_read": [],
        "calculation_steps": ""
    },
    "max_speed": "",
    "pull_up_required": true,
    "source_page": 0
}
```

**I2C Address Calculation Guide:**

| Format in Datasheet | Example | Calculation | 7-bit Address |
|---------------------|---------|-------------|---------------|
| `001000x` | x=AD0 | 0b0010000=0x10, 0b0010001=0x11 | 0x10/0x11 |
| `11010xx` | xx=A1A0 | 0b1101000=0x68 to 0b1101011=0x6B | 0x68-0x6B |
| `0x20` (8-bit write) | - | 0x20 >> 1 | 0x10 |
| `0xD0` (8-bit write) | - | 0xD0 >> 1 | 0x68 |

**Example Address Calculation:**
```json
{
    "format_shown": "001000x",
    "format_explanation": "where x equals AD0 pin state",
    "address_7bit": ["0x10", "0x11"],
    "calculation_steps": [
        "AD0 = 0: 0010000 binary = 0x10",
        "AD0 = 1: 0010001 binary = 0x11"
    ]
}
```

**Common I2C Device Addresses** *(validation reference — cross-check extracted address against these known values; do not output as fact without verifying against the PDF)*:

| Device Type | Common Addresses |
|-------------|------------------|
| I2C EEPROM (24Cxx) | 0x50-0x57 |
| I2C RTC (DS3231, PCF8563) | 0x51, 0x68 |
| I2C Temp Sensor (LM75) | 0x48-0x4F |
| I2C ADC (ADS1115) | 0x48-0x4B |
| I2C IMU (MPU6050) | 0x68-0x69 |
| I2C Port Expander (MCP23017) | 0x20-0x27 |

---

## SPI Interface Template

```json
{
    "_template": "spi_interface",
    "_version": "1.0",
    "interface_type": "SPI",
    "pins": {
        "mosi": "",
        "miso": "",
        "sck": "",
        "cs": ""
    },
    "modes_supported": [],
    "max_speed": "",
    "source_page": 0
}
```

---

## Electrical Specs Template

```json
{
    "_template": "electrical_specs",
    "_version": "1.0",
    "absolute_maximum": [
        {
            "parameter": "",
            "min": "",
            "max": "",
            "unit": "",
            "notes": "",
            "source": ""
        }
    ],
    "recommended_operating": [
        {
            "parameter": "",
            "min": "",
            "typ": "",
            "max": "",
            "unit": "",
            "conditions": "",
            "source": ""
        }
    ],
    "key_parameters": [
        {
            "parameter": "",
            "min": "",
            "typ": "",
            "max": "",
            "unit": "",
            "conditions": "",
            "footnotes": [],
            "source": ""
        }
    ]
}
```

**Extraction Rules:**
- Extract raw values without transformation
- Include column name (Min/Typ/Max)
- Note test conditions
- Check for footnotes (often contain critical constraints)
- Cite source: page number and table name

---

## Raw Extraction Value Format

Each extracted value MUST include source information:

```json
{
    "parameter": "DAC SNR",
    "value": "93",
    "unit": "dB",
    "column": "Typ",
    "min": "85",
    "max": "95",
    "conditions": "A-weighted, 24-bit",
    "page": 8,
    "table_name": "DAC Performance",
    "confidence": "HIGH"
}
```

**Confidence Levels:**

| Level | Definition | Example |
|-------|------------|---------|
| **HIGH** | Direct read from clear table, verified by re-read | "93 dB" from clean table |
| **MEDIUM** | Some ambiguity (OCR issues, merged cells) | Value from slightly blurry OCR |
| **LOW** | Inferred from context, multiple interpretations | Value estimated from graph |
| **UNVERIFIED** | Extracted but not yet verified | Initial extraction before validation |
