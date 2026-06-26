---
name: senseaudio-audio-quality-checker
description: Analyze audio quality, detect noise types, and provide improvement recommendations. Use when users need to check audio quality, validate recordings, or identify audio problems.
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio Audio Quality Checker

Analyze audio files to detect quality issues, identify noise types, and provide improvement recommendations.

## What This Skill Does

- Detect noise and quality issues in audio files
- Identify specific noise types (background noise, hum, static, etc.)
- Provide noise severity ratings
- Generate quality assessment reports
- Recommend improvements for audio quality

## Prerequisites

Install required Python packages:

```bash
pip install requests
```


## Implementation Guide

### Step 1: Analyze Audio File

```python
import os
import requests

API_KEY = os.environ["SENSEAUDIO_API_KEY"]

def check_audio_quality(audio_file):
    url = "https://api.senseaudio.cn/v1/audio/analysis"

    headers = {"Authorization": f"Bearer {API_KEY}"}
    files = {"file": open(audio_file, "rb")}
    data = {"model": "sense-asr-check"}

    response = requests.post(url, headers=headers, files=files, data=data)
    return response.json()

# Example response:
# {
#   "audio_info": {
#     "duration": 5230,
#     "format": "wav"
#   },
#   "result": {
#     "has_noise": true,
#     "noise_score": 0.65,
#     "severity": "moderate",
#     "noise_types": ["background_noise", "hum"],
#     "analysis": "Audio contains moderate background noise and electrical hum"
#   }
# }
```

### Step 2: Parse Quality Report

```python
def parse_quality_report(analysis_result):
    audio_info = analysis_result.get("audio_info", {})
    result = analysis_result.get("result", {})

    report = {
        "duration_ms": audio_info.get("duration"),
        "format": audio_info.get("format"),
        "has_issues": result.get("has_noise", False),
        "noise_score": result.get("noise_score", 0),
        "severity": result.get("severity", "none"),
        "noise_types": result.get("noise_types", []),
        "analysis": result.get("analysis", ""),
        "recommendations": generate_recommendations(result)
    }

    return report
```

### Step 3: Generate Recommendations

```python
def generate_recommendations(quality_result):
    recommendations = []

    noise_score = quality_result.get("noise_score", 0)
    noise_types = quality_result.get("noise_types", [])
    severity = quality_result.get("severity", "none")

    # General recommendations based on severity
    if severity == "severe":
        recommendations.append("Re-record audio in a quieter environment")
        recommendations.append("Use professional audio equipment")
    elif severity == "moderate":
        recommendations.append("Apply noise reduction in post-processing")
        recommendations.append("Consider using a better microphone")
    elif severity == "mild":
        recommendations.append("Minor noise reduction may improve quality")

    # Specific recommendations based on noise types
    if "background_noise" in noise_types:
        recommendations.append("Record in a quieter location")
        recommendations.append("Use acoustic treatment (foam panels, curtains)")

    if "hum" in noise_types:
        recommendations.append("Check for electrical interference")
        recommendations.append("Use balanced audio cables")
        recommendations.append("Ensure proper grounding of equipment")

    if "static" in noise_types:
        recommendations.append("Check cable connections")
        recommendations.append("Replace faulty cables or equipment")

    if "wind_noise" in noise_types:
        recommendations.append("Use a windscreen or pop filter")
        recommendations.append("Record indoors or in sheltered location")

    if "echo" in noise_types:
        recommendations.append("Add acoustic treatment to reduce reflections")
        recommendations.append("Record closer to microphone")

    return recommendations
```

### Step 4: Batch Quality Check

```python
def batch_quality_check(audio_files):
    results = []

    for audio_file in audio_files:
        try:
            analysis = check_audio_quality(audio_file)
            report = parse_quality_report(analysis)

            results.append({
                "file": audio_file,
                "status": "analyzed",
                "report": report
            })
        except Exception as e:
            results.append({
                "file": audio_file,
                "status": "error",
                "error": str(e)
            })

    return results
```

## Advanced Features

### Quality Scoring System

```python
def calculate_quality_score(analysis_result):
    """Calculate overall quality score (0-100)"""
    noise_score = analysis_result.get("noise_score", 0)
    severity = analysis_result.get("severity", "none")

    # Base score
    base_score = 100

    # Deduct based on noise score
    noise_penalty = noise_score * 50  # Max 50 points

    # Additional penalty for severity
    severity_penalties = {
        "none": 0,
        "mild": 10,
        "moderate": 25,
        "severe": 40
    }
    severity_penalty = severity_penalties.get(severity, 0)

    final_score = max(0, base_score - noise_penalty - severity_penalty)

    return {
        "score": round(final_score, 1),
        "grade": get_quality_grade(final_score)
    }

def get_quality_grade(score):
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 60:
        return "Fair"
    elif score >= 40:
        return "Poor"
    else:
        return "Unacceptable"
```

### Comparative Analysis

```python
def compare_audio_quality(original_file, processed_file):
    """Compare quality before and after processing"""

    original_analysis = check_audio_quality(original_file)
    processed_analysis = check_audio_quality(processed_file)

    original_score = calculate_quality_score(original_analysis["result"])
    processed_score = calculate_quality_score(processed_analysis["result"])

    comparison = {
        "original": {
            "file": original_file,
            "score": original_score,
            "noise_score": original_analysis["result"]["noise_score"]
        },
        "processed": {
            "file": processed_file,
            "score": processed_score,
            "noise_score": processed_analysis["result"]["noise_score"]
        },
        "improvement": {
            "score_delta": processed_score["score"] - original_score["score"],
            "noise_reduction": original_analysis["result"]["noise_score"] - processed_analysis["result"]["noise_score"]
        }
    }

    return comparison
```

### Automated Quality Gate

```python
def quality_gate_check(audio_file, min_score=70):
    """Check if audio meets minimum quality threshold"""

    analysis = check_audio_quality(audio_file)
    quality = calculate_quality_score(analysis["result"])

    passed = quality["score"] >= min_score

    return {
        "passed": passed,
        "score": quality["score"],
        "grade": quality["grade"],
        "threshold": min_score,
        "analysis": analysis
    }
```

### Detailed Report Generation

```python
def generate_detailed_report(audio_file):
    """Generate comprehensive quality report"""

    analysis = check_audio_quality(audio_file)
    report = parse_quality_report(analysis)
    quality = calculate_quality_score(analysis["result"])

    detailed_report = f"""
# Audio Quality Report

## File Information
- **File**: {audio_file}
- **Duration**: {report['duration_ms']/1000:.2f} seconds
- **Format**: {report['format']}

## Quality Assessment
- **Overall Score**: {quality['score']}/100
- **Grade**: {quality['grade']}
- **Noise Score**: {report['noise_score']:.2f}
- **Severity**: {report['severity']}

## Issues Detected
{'- ' + '\\n- '.join(report['noise_types']) if report['noise_types'] else 'No issues detected'}

## Analysis
{report['analysis']}

## Recommendations
{'- ' + '\\n- '.join(report['recommendations']) if report['recommendations'] else 'No recommendations'}
"""

    return detailed_report
```

## Use Cases

### Pre-Recording Validation

```python
def validate_recording_environment():
    """Test recording environment before actual recording"""

    # record_test_audio() is a placeholder — implement using your preferred
    # audio capture library (e.g. sounddevice, pyaudio) to record a short clip.
    test_file = record_test_audio(duration=5)

    # Check quality
    gate_result = quality_gate_check(test_file, min_score=75)

    if gate_result["passed"]:
        return {
            "ready": True,
            "message": "Environment is suitable for recording"
        }
    else:
        return {
            "ready": False,
            "message": "Environment needs improvement",
            "recommendations": gate_result["analysis"]["result"]["recommendations"]
        }
```

### Post-Production Quality Control

```python
def qc_pipeline(audio_files, min_score=80):
    """Quality control for batch of audio files"""

    qc_results = {
        "passed": [],
        "failed": [],
        "total": len(audio_files)
    }

    for audio_file in audio_files:
        result = quality_gate_check(audio_file, min_score)

        if result["passed"]:
            qc_results["passed"].append(audio_file)
        else:
            qc_results["failed"].append({
                "file": audio_file,
                "score": result["score"],
                "issues": result["analysis"]["result"]["noise_types"]
            })

    qc_results["pass_rate"] = len(qc_results["passed"]) / qc_results["total"] * 100

    return qc_results
```

## Output Format

- Quality analysis JSON
- Detailed quality report (Markdown/PDF)
- Noise detection results
- Improvement recommendations
- Quality score and grade

## Tips for Best Results

- Test audio files before important recordings
- Use quality gates in production pipelines
- Compare before/after processing
- Track quality metrics over time
- Address severe issues immediately

## Example Usage

**User request**: "Check the quality of this audio recording and tell me if it's good enough for a podcast"

**Skill actions**:
1. Upload audio file to analysis API
2. Parse quality results
3. Calculate quality score
4. Generate recommendations
5. Provide clear pass/fail assessment
6. Suggest improvements if needed

## Reference

API docs: https://senseaudio.cn/docs/speech_recognition
