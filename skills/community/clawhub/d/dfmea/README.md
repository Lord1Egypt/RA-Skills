# DFMEA - Design Failure Mode and Effects Analysis

A comprehensive OpenClaw skill for performing Design Failure Mode and Effects Analysis (DFMEA) in quality engineering and product development.

## Overview

DFMEA is a systematic approach used to identify potential failure modes in a design, assess their impact, and implement preventive measures. This skill helps engineers and quality professionals:

- Create structured DFMEA analyses
- Calculate Risk Priority Numbers (RPN)
- Generate mitigation strategies
- Track action items and improvements
- Export reports in various formats

## Key Features

### 1. DFMEA Template Creation
- Automatically generates standardized DFMEA templates
- Supports custom process steps and components
- Includes industry-standard severity, occurrence, and detection scales

### 2. Risk Assessment
- Calculates RPN = Severity × Occurrence × Detection
- Provides risk categorization (High/Medium/Low)
- Highlights critical failure modes requiring immediate attention

### 3. Mitigation Planning
- Suggests preventive and detective actions
- Tracks action effectiveness
- Supports iterative improvement cycles

### 4. Reporting & Export
- Generates comprehensive DFMEA reports
- Exports to CSV, JSON, or Markdown formats
- Creates visual risk heat maps

## Usage Examples

### Basic DFMEA Analysis
```
Create a DFMEA for automotive brake system design
```

### Specific Component Analysis
```
Perform DFMEA on electric vehicle battery thermal management system
```

### Risk Prioritization
```
Analyze the top 5 highest risk failure modes in our medical device design
```

### Action Tracking
```
Generate mitigation actions for failure modes with RPN > 100
```

## DFMEA Structure

Each DFMEA analysis includes:

1. **Item/Function**: The component or process being analyzed
2. **Failure Mode**: How the item could fail
3. **Failure Effects**: Impact of the failure
4. **Severity (S)**: Rating 1-10 (10 = most severe)
5. **Causes**: Root causes of the failure mode
6. **Occurrence (O)**: Rating 1-10 (10 = most likely)
7. **Current Controls**: Existing prevention/detection measures
8. **Detection (D)**: Rating 1-10 (10 = least detectable)
9. **RPN**: Risk Priority Number = S × O × D
10. **Recommended Actions**: Mitigation strategies
11. **Responsibility**: Who owns the action
12. **Target Date**: When action should be completed

## Industry Standards Supported

- AIAG/VDA FMEA Handbook (2019)
- ISO 9001 Quality Management
- IATF 16949 Automotive Quality
- AS9100 Aerospace Quality
- ISO 13485 Medical Device Quality

## Smart Hardware Industry Support

This skill includes specialized templates and analysis frameworks for smart hardware applications:

- **IoT Device Security**: Authentication vulnerabilities, data privacy risks
- **Wireless Connectivity**: WiFi/Bluetooth/Zigbee reliability issues
- **Power Management**: Battery safety, charging circuit failures
- **Sensor Accuracy**: Calibration drift, environmental interference
- **Firmware Updates**: OTA security, rollback mechanisms

## Installation

This skill is automatically available when installed in your OpenClaw workspace.

## License

MIT License - Free to use and modify.