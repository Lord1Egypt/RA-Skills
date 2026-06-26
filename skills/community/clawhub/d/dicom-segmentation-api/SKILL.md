# DICOM Segmentation API

Deploy medical image segmentation API using TotalSegmentator and MONAI.

## Features

- TotalSegmentator integration (117 body structures)
- MONAI workflow support
- Fast API server
- DICOM file upload
- 3D model export (GLB format)
- Statistics generation
- Batch processing

## Usage

```bash
# Start server
python api_server.py

# Or with custom port
python api_server.py --port 8000
```

## API Endpoints

- `POST /api/segment` - Upload DICOM for segmentation
- `GET /api/task/{task_id}` - Get task status
- `GET /api/result/{task_id}` - Get segmentation result
- `GET /health` - Health check

## Requirements

- Python 3.8+
- CUDA (optional, for GPU acceleration)
- 8GB RAM minimum

## Models

- TotalSegmentator: 117 body structures
- MONAI: whole-body-3mm, organ, tumor models

## Author

Sunshine-del-ux
