import sys
import os
import functools
import cv2
import torch

print = functools.partial(print, flush=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from depth_anything_v2.dpt import DepthAnythingV2

MODEL_CONFIGS = {
    'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
    'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
    'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
    'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]},
}


def main():
    model_path = sys.argv[1] if len(sys.argv) > 1 else 'depth_anything_v2_vitb.pth'
    video_path = sys.argv[2] if len(sys.argv) > 2 else 'input.mp4'
    out_path = sys.argv[3] if len(sys.argv) > 3 else 'depth_video.mp4'
    encoder = sys.argv[4] if len(sys.argv) > 4 else 'vitb'
    if encoder not in MODEL_CONFIGS:
        print('[error] unknown encoder:', encoder, '| 可选:', ', '.join(MODEL_CONFIGS))
        sys.exit(1)
    max_frames = 0
    if len(sys.argv) > 5:
        try:
            max_frames = int(sys.argv[5])  # 0 = 全部帧
        except ValueError:
            print('[warn] invalid max_frames, using 0 (全部帧)')
            max_frames = 0

    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    print('[info] device =', DEVICE)
    print('[info] loading model ...')
    model = DepthAnythingV2(**MODEL_CONFIGS[encoder])
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model = model.to(DEVICE).eval()
    print('[info] model loaded')

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print('[error] cannot open video:', video_path)
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps != fps or fps <= 0:  # 处理 0 / NaN / 负数
        print('[warn] invalid fps, fallback to 24.0')
        fps = 24.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if max_frames > 0:
        total = min(total, max_frames)
    print('[info] video: %dx%d @ %.2f fps, %d frames' % (width, height, fps, total))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height), isColor=False)
    if not writer.isOpened():
        print('[error] cannot create video writer:', out_path)
        cap.release()
        sys.exit(1)

    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        depth = model.infer_image(frame)
        dmin, dmax = float(depth.min()), float(depth.max())
        depth_norm = ((depth - dmin) / (dmax - dmin + 1e-8) * 255.0).astype('uint8')
        writer.write(depth_norm)
        idx += 1
        if idx % 10 == 0 or idx == total:
            print('[progress] frame %d/%d (depth %.1f-%.1f)' % (idx, total, dmin, dmax))
        if max_frames > 0 and idx >= max_frames:
            break

    cap.release()
    writer.release()
    print('[ok] saved depth video ->', out_path, '(%d frames)' % idx)


if __name__ == '__main__':
    main()
