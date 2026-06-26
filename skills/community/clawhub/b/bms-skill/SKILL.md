# BMS CAN Analyzer Skill

A specialized skill for parsing automotive BMS (Battery Management System) BLF files and extracting time series data for specific signals using DBC definitions.

## When to Use

✅ **USE this skill when:**

- "Extract voltage signal from my BLF file"
- "Get temperature readings over time from CAN log"
- "Parse BMS data using my DBC file"
- "Show SOC time series from automotive log"
- "Analyze specific CAN signal from BLF recording"

## Requirements

- BLF (Binary Logging Format) file containing CAN messages
- DBC (Database CAN) file with signal definitions
- Signal name to extract (must match DBC definition)

## Commands

### Extract Single Signal Time Series

```bash
# Basic usage
bms-can-analyzer --blf-file path/to/log.blf --dbc-file path/to/definitions.dbc --signal-name "Cell_Voltage_1"

# With output format
bms-can-analyzer --blf-file log.blf --dbc-file defs.dbc --signal-name "Pack_Temperature" --output-format json

# Save to file
bms-can-analyzer --blf-file log.blf --dbc-file defs.dbc --signal-name "SOC" --output-file soc_data.csv
```

### Extract Multiple Signals

```bash
# Comma-separated signal names
bms-can-analyzer --blf-file log.blf --dbc-file defs.dbc --signal-name "Cell_Voltage_1,Cell_Voltage_2,Cell_Temp_1"
```

### Supported Output Formats

- `csv` - Comma-separated values (default)
- `json` - JSON array with timestamp and value pairs
- `text` - Simple text format with timestamp and value

## Signal Name Requirements

Signal names must exactly match those defined in your DBC file. Common BMS signal examples:

- `Cell_Voltage_1`, `Cell_Voltage_2`, ..., `Cell_Voltage_N`
- `Cell_Temperature_1`, `Cell_Temperature_2`, ..., `Cell_Temperature_N`
- `Pack_Voltage`, `Pack_Current`, `Pack_Temperature`
- `State_of_Charge`, `State_of_Health`
- `Max_Cell_Voltage`, `Min_Cell_Voltage`
- `Max_Cell_Temp`, `Min_Cell_Temp`

## Error Handling

- **File not found**: Check BLF and DBC file paths
- **Signal not found**: Verify signal name matches DBC definition exactly
- **Corrupted BLF**: File may be incomplete or damaged
- **Invalid DBC**: DBC syntax errors will prevent parsing

## Dependencies

This skill requires:
- Python 3.7+
- `python-can` library
- `cantools` library
- `blf` library (for BLF parsing)

The skill will automatically install these dependencies if not present.