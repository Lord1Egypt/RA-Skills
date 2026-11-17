import sys
import os
import cv2
import torch

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
    image_path = sys.argv[2] if len(sys.argv) > 2 else 'input.png'
    out_path = sys.argv[3] if len(sys.argv) > 3 else 'depth.png'
    encoder = sys.argv[4] if len(sys.argv) > 4 else 'vitb'
    if encoder not in MODEL_CONFIGS:
        print('[error] unknown encoder:', encoder, '| 可选:', ', '.join(MODEL_CONFIGS))
        sys.exit(1)

    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    print('[info] device =', DEVICE)
    print('[info] loading model ...')
    model = DepthAnythingV2(**MODEL_CONFIGS[encoder])
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model = model.to(DEVICE).eval()
    print('[info] model loaded')

    raw_img = cv2.imread(image_path)
    if raw_img is None:
        print('[error] cannot read image:', image_path)
        sys.exit(1)

    depth = model.infer_image(raw_img)
    print('[info] depth shape =', depth.shape, 'min=%.3f' % depth.min(), 'max=%.3f' % depth.max())

    depth_norm = (depth - depth.min()) / (depth.max() - depth.min() + 1e-8) * 255.0
    depth_norm = depth_norm.astype('uint8')
    cv2.imwrite(out_path, depth_norm)
    print('[ok] saved grayscale depth ->', out_path)

    color_out = os.path.splitext(out_path)[0] + '_color.png'
    cv2.imwrite(color_out, cv2.applyColorMap(depth_norm, cv2.COLORMAP_INFERNO))
    print('[ok] saved color depth ->', color_out)


if __name__ == '__main__':
    main()
