# Platform Notes

## Tested environments

### Windows
- OS: Windows 11
- GPU: NVIDIA GeForce GTX 1060 6GB
- OpenClaw install mode: installed directly on Windows
- Camera backend: DirectShow

### Linux
- OS: Linux (generic)
- GPU: varies
- OpenClaw install mode: installed directly on Linux
- Camera backend: V4L2

## Model location

Store the YOLO model in `workspace/assets/yolo/` or configure the path in `TOOLS.md`.

## Camera device detection

### Linux
Check available camera devices:
```bash
ls /dev/video*
```
Typical laptop webcam appears as `/dev/video0` or `/dev/video1`.

Make sure the user has read access to the device, or add the user to the `video` group.

### Windows
Camera index `0` is typically the built-in notebook webcam. If multiple cameras exist, test indices starting from `0`.

## Maintenance notes

If the webcam index changes or multiple cameras appear, test camera indices manually.

If the GPU stack changes, verify:
- `torch.cuda.is_available()`
- model inference still works
- saved images still land under `workspace/tmp/`

## Suggested output folders

- Raw webcam captures: `workspace/tmp/camshots/`
- Annotated YOLO captures: `workspace/tmp/yolo-captures/`
