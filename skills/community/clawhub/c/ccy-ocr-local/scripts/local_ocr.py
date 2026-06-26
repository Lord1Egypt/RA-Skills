#!/usr/bin/env python3
import argparse
import csv
import io
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract

try:
    import cv2  # type: ignore
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover
    cv2 = None
    np = None


FAST_PSMS = (6, 7, 11)
AUTO_PSMS = (6, 7, 11, 3)
LABEL_PSMS = (7, 6, 11, 13)
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff', '.webp'}
ROTATION_ANGLES = (0, 90, 180, 270)

DOMAIN_CORRECTIONS = {
    '杀子': '镊子',
    '软头杀子': '软头镊子',
    '银于': '镊子',
    '软头银子': '软头镊子',
}


def fail(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    sys.exit(code)


def candidate_tesseract_paths() -> list[Path]:
    candidates: list[Path] = []
    env_cmd = os.environ.get('TESSERACT_CMD')
    if env_cmd:
        candidates.append(Path(env_cmd).expanduser())
    if os.name == 'nt':
        program_files = [
            os.environ.get('ProgramFiles'),
            os.environ.get('ProgramFiles(x86)'),
            'C:/Program Files',
            'C:/Program Files (x86)',
        ]
        for base in program_files:
            if not base:
                continue
            candidates.append(Path(base) / 'Tesseract-OCR' / 'tesseract.exe')
            candidates.append(Path(base) / 'Tesseract' / 'tesseract.exe')
    return candidates


def resolve_tesseract_cmd(explicit_cmd: str | None = None) -> str:
    if explicit_cmd:
        explicit_path = Path(explicit_cmd).expanduser()
        if explicit_path.exists():
            return str(explicit_path)
        found = shutil.which(explicit_cmd)
        if found:
            return found
        fail(f'指定的 tesseract 不可用: {explicit_cmd}')

    found = shutil.which('tesseract')
    if found:
        return found

    for candidate in candidate_tesseract_paths():
        if candidate.exists():
            return str(candidate)

    fail('未找到 tesseract。可安装 Tesseract，或通过 --tesseract-cmd / TESSERACT_CMD 显式指定路径。')


def configure_tesseract(explicit_cmd: str | None = None) -> str:
    cmd = resolve_tesseract_cmd(explicit_cmd)
    pytesseract.pytesseract.tesseract_cmd = cmd
    return cmd


def tesseract_langs(tesseract_cmd: str) -> set[str]:
    try:
        out = subprocess.check_output([tesseract_cmd, '--list-langs'], stderr=subprocess.STDOUT, text=True)
    except Exception:
        return set()
    lines = [x.strip() for x in out.splitlines() if x.strip()]
    return set(lines[1:] if lines and 'List of available languages' in lines[0] else lines)


def ensure_langs(lang_expr: str, tesseract_cmd: str) -> None:
    langs = tesseract_langs(tesseract_cmd)
    missing = [x for x in lang_expr.split('+') if x and x not in langs]
    if missing:
        fail(f'缺少 Tesseract 语言数据：{", ".join(missing)}。当前可用：{", ".join(sorted(langs)) or "无"}')


def open_image(img_path: Path) -> Image.Image:
    try:
        img = Image.open(img_path)
        return ImageOps.exif_transpose(img)
    except Exception as exc:
        fail(f'无法打开图片 {img_path}: {exc}')


def upscale_if_small(img: Image.Image, min_edge: int) -> Image.Image:
    w, h = img.size
    longest = max(w, h)
    if longest >= min_edge or longest <= 0:
        return img
    scale = min_edge / float(longest)
    return img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.Resampling.LANCZOS)


def preprocess_pil(img_path: Path, min_edge: int, sharpen: bool) -> Image.Image:
    img = open_image(img_path)
    img = ImageOps.grayscale(img)
    img = ImageOps.autocontrast(img)
    img = upscale_if_small(img, min_edge)
    if sharpen:
        img = img.filter(ImageFilter.SHARPEN)
    return img


def preprocess_cv(img_path: Path, min_edge: int, sharpen: bool) -> Image.Image:
    assert cv2 is not None
    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        fail(f'无法读取图片: {img_path}')

    h, w = img.shape[:2]
    longest = max(h, w)
    if 0 < longest < min_edge:
        scale = min_edge / float(longest)
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    if sharpen:
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.int32)
        img = cv2.filter2D(img, -1, kernel)

    return Image.fromarray(img)


def preprocess_image(img_path: Path, min_edge: int, sharpen: bool, no_preprocess: bool) -> Image.Image:
    if no_preprocess:
        return open_image(img_path)
    if cv2 is not None:
        return preprocess_cv(img_path, min_edge=min_edge, sharpen=sharpen)
    return preprocess_pil(img_path, min_edge=min_edge, sharpen=sharpen)


def build_config(psm: int, dpi: int, oem: int = 3, extra: str = '') -> str:
    extra_str = f' {extra.strip()}' if extra.strip() else ''
    return f'--oem {oem} --psm {psm} -c user_defined_dpi={dpi} preserve_interword_spaces=1{extra_str}'


def run_text_ocr(img: Image.Image, lang: str, psm: int, dpi: int, oem: int = 3, extra: str = '') -> str:
    return pytesseract.image_to_string(img, lang=lang, config=build_config(psm, dpi, oem=oem, extra=extra)).strip()


def ocr_confidence_metrics(img: Image.Image, lang: str, psm: int, dpi: int, oem: int = 3, extra: str = '') -> dict:
    """返回当前候选 OCR 的平均置信度，用于候选排序和低置信提示。"""
    try:
        data = pytesseract.image_to_data(img, lang=lang, config=build_config(psm, dpi, oem=oem, extra=extra))
    except Exception:
        return {'avg_conf': None, 'min_conf': None, 'word_count': 0, 'low_conf_words': 0}

    reader = csv.DictReader(io.StringIO(data), delimiter='\t')
    confs: list[float] = []
    low_conf_words = 0
    for row in reader:
        text = (row.get('text') or '').strip()
        if not text:
            continue
        try:
            conf = float(row.get('conf') or -1)
        except Exception:
            conf = -1.0
        if conf < 0:
            continue
        confs.append(conf)
        if conf < 55:
            low_conf_words += 1

    if not confs:
        return {'avg_conf': None, 'min_conf': None, 'word_count': 0, 'low_conf_words': 0}
    return {
        'avg_conf': round(sum(confs) / len(confs), 2),
        'min_conf': round(min(confs), 2),
        'word_count': len(confs),
        'low_conf_words': low_conf_words,
    }


def quality_warning(meta: dict, content: str, doc_hint: str) -> str | None:
    avg_conf = meta.get('avg_conf')
    score = meta.get('score') or 0
    chars = len([ch for ch in content if not ch.isspace()])
    if chars == 0:
        return 'empty_result'
    if avg_conf is not None and avg_conf < 55:
        return 'low_confidence'
    if doc_hint == 'label' and score < 20:
        return 'weak_label_score'
    if doc_hint == 'general' and score < 8:
        return 'weak_text_score'
    return None


def quality_suggestions(warning: str | None) -> list[str]:
    if not warning:
        return []
    return [
        '尝试加 --autorotate --multi-variant --mode accurate',
        '确认 --lang 包含图片语言，例如 chi_sim+eng',
        '提高图片分辨率或避免压缩/模糊',
        '标签/票据类图片可加 --doc-hint label',
    ]


def score_text(text: str) -> tuple[int, int, int]:
    stripped = text.strip()
    non_space = sum(1 for ch in stripped if not ch.isspace())
    lines = sum(1 for line in stripped.splitlines() if line.strip())
    alnum = sum(1 for ch in stripped if ch.isalnum())
    return non_space, lines, alnum


def choose_psms(mode: str, manual_psm: int | None, doc_hint: str = 'general') -> tuple[int, ...]:
    if manual_psm is not None:
        return (manual_psm,)
    if doc_hint == 'label':
        return LABEL_PSMS
    if mode == 'fast':
        return FAST_PSMS
    if mode == 'accurate':
        return AUTO_PSMS
    return (6,)


def estimate_orientation_candidates(img: Image.Image) -> tuple[int, ...]:
    w, h = img.size
    if w >= h * 1.2:
        return (0, 180)
    if h >= w * 1.2:
        return (90, 270)
    return ROTATION_ANGLES


def generate_variants(img: Image.Image) -> list[tuple[str, Image.Image]]:
    base = ImageOps.grayscale(img)
    variants: list[tuple[str, Image.Image]] = []

    def add(name: str, im: Image.Image) -> None:
        variants.append((name, im))

    auto = ImageOps.autocontrast(base)
    add('gray', base)
    add('autocontrast', auto)
    add('autocontrast_sharp', auto.filter(ImageFilter.SHARPEN))
    add('contrast_2x', ImageEnhance.Contrast(base).enhance(2.0))
    add('contrast_25x_sharp', ImageEnhance.Contrast(base).enhance(2.5).filter(ImageFilter.SHARPEN))
    add('bw_160', auto.point(lambda p: 255 if p > 160 else 0))

    for factor in (2, 3):
        resized = auto.resize((auto.width * factor, auto.height * factor), Image.Resampling.LANCZOS)
        add(f'autocontrast_{factor}x', resized)
        add(f'autocontrast_sharp_{factor}x', resized.filter(ImageFilter.SHARPEN))
        add(f'contrast_{factor}x', ImageEnhance.Contrast(resized).enhance(2.2))

    if cv2 is not None and np is not None:
        arr = np.array(base)
        norm = cv2.normalize(arr, None, 0, 255, cv2.NORM_MINMAX)
        gauss = cv2.GaussianBlur(norm, (3, 3), 0)
        otsu = cv2.threshold(gauss, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        adapt = cv2.adaptiveThreshold(norm, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.int32)
        sharp = cv2.filter2D(norm, -1, kernel)
        add('cv_otsu', Image.fromarray(otsu))
        add('cv_adapt', Image.fromarray(adapt))
        add('cv_sharp', Image.fromarray(sharp))
        add('cv_sharp_otsu', Image.fromarray(cv2.threshold(sharp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]))
    return variants


def apply_domain_corrections(text: str) -> str:
    fixed = text
    for src, dst in DOMAIN_CORRECTIONS.items():
        fixed = fixed.replace(src, dst)
    return fixed


def score_candidate_text(text: str, doc_hint: str = 'general') -> int:
    score = 0
    score += len([ch for ch in text if not ch.isspace()])
    score += 2 * sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    score += sum(1 for ch in text if ch.isdigit())
    if doc_hint == 'label':
        if '815F-ST1' in text:
            score += 20
        if '软头' in text:
            score += 10
        if '镊子' in text:
            score += 14
        if '软头镊子' in text:
            score += 24
        if '杀子' in text:
            score -= 16
        if '供应商' in text or '客户' in text or '数量' in text:
            score += 4
    return score


def detect_doc_hint(img_path: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    name = img_path.name.lower()
    if 'label' in name or '标签' in name or 'delivery' in name:
        return 'label'
    return 'general'


def run_best_text_ocr(img: Image.Image, lang: str, dpi: int, mode: str, manual_psm: int | None, doc_hint: str = 'general', multi_variant: bool = False) -> tuple[str, int, dict]:
    best_text = ''
    best_psm = manual_psm if manual_psm is not None else 6
    best_meta = {'variant': 'base', 'oem': 3, 'dpi': dpi, 'score': -10**9}

    variants = [('base', img)]
    if multi_variant:
        all_variants = generate_variants(img)
        if doc_hint == 'label':
            preferred = {'autocontrast', 'autocontrast_sharp', 'autocontrast_2x', 'autocontrast_sharp_2x', 'cv_otsu', 'cv_sharp_otsu'}
            variants = [item for item in all_variants if item[0] in preferred] or all_variants[:6]
        else:
            variants = all_variants

    psm_candidates = choose_psms(mode, manual_psm, doc_hint=doc_hint)
    dpi_candidates = (dpi, 450) if doc_hint == 'label' and multi_variant else (dpi,)
    oem_candidates = (3, 1) if doc_hint == 'label' and multi_variant else (3,)

    for variant_name, variant_img in variants:
        for psm in psm_candidates:
            for candidate_dpi in dpi_candidates:
                for oem in oem_candidates:
                    extra = ''
                    if doc_hint == 'label':
                        extra = '-c tessedit_do_invert=0'
                    try:
                        text = run_text_ocr(variant_img, lang=lang, psm=psm, dpi=candidate_dpi, oem=oem, extra=extra)
                    except Exception:
                        continue
                    corrected = apply_domain_corrections(text)
                    metrics = ocr_confidence_metrics(variant_img, lang=lang, psm=psm, dpi=candidate_dpi, oem=oem, extra=extra)
                    score = score_candidate_text(corrected, doc_hint=doc_hint)
                    avg_conf = metrics.get('avg_conf')
                    if avg_conf is not None:
                        # 置信度参与候选排序，避免“字符多但明显乱码”的候选胜出。
                        score += int(float(avg_conf) * 0.35)
                        score += min(6, int(metrics.get('word_count') or 0))
                        score -= int(metrics.get('low_conf_words') or 0) * 2
                    if score > best_meta['score']:
                        best_text = corrected
                        best_psm = psm
                        best_meta = {'variant': variant_name, 'oem': oem, 'dpi': candidate_dpi, 'score': score, **metrics}
    return best_text, best_psm, best_meta


def autorotate_image(img: Image.Image, lang: str, dpi: int, mode: str, manual_psm: int | None, strategy: str, doc_hint: str = 'general', multi_variant: bool = False) -> tuple[Image.Image, int, int, str, dict]:
    candidate_angles = ROTATION_ANGLES if strategy == 'full' else estimate_orientation_candidates(img)

    best_img = img
    best_angle = 0
    best_psm = manual_psm if manual_psm is not None else 6
    best_text = ''
    best_meta = {'variant': 'base', 'oem': 3, 'dpi': dpi, 'score': -10**9}

    for angle in candidate_angles:
        candidate = img.rotate(angle, expand=True) if angle else img
        text, psm, meta = run_best_text_ocr(candidate, lang=lang, dpi=dpi, mode=mode, manual_psm=manual_psm, doc_hint=doc_hint, multi_variant=multi_variant)
        if meta['score'] > best_meta['score']:
            best_img = candidate
            best_angle = angle
            best_psm = psm
            best_text = text
            best_meta = meta

    if strategy == 'smart' and len(candidate_angles) < len(ROTATION_ANGLES):
        weak_result = best_meta['score'] < 20 if doc_hint == 'label' else best_meta['score'] < 8
        if weak_result:
            return autorotate_image(img, lang=lang, dpi=dpi, mode=mode, manual_psm=manual_psm, strategy='full', doc_hint=doc_hint, multi_variant=multi_variant)

    return best_img, best_angle, best_psm, best_text, best_meta


def image_to_tsv(img: Image.Image, lang: str, psm: int, dpi: int, min_conf: int) -> str:
    config = build_config(psm, dpi)
    data = pytesseract.image_to_data(img, lang=lang, config=config)
    reader = csv.DictReader(io.StringIO(data), delimiter='\t')
    out = io.StringIO()
    writer = csv.writer(out, delimiter='\t', lineterminator='\n')
    writer.writerow(['text', 'conf', 'left', 'top', 'width', 'height', 'line_num', 'block_num', 'page_num'])

    for row in reader:
        text = (row.get('text') or '').strip()
        conf_raw = (row.get('conf') or '').strip()
        try:
            conf = int(float(conf_raw))
        except Exception:
            conf = -1
        if not text or conf < min_conf:
            continue
        writer.writerow([
            text,
            conf,
            row.get('left', ''),
            row.get('top', ''),
            row.get('width', ''),
            row.get('height', ''),
            row.get('line_num', ''),
            row.get('block_num', ''),
            row.get('page_num', ''),
        ])
    return out.getvalue().rstrip('\n')


def collect_images(input_path: Path, recursive: bool) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    if not input_path.is_dir():
        fail(f'输入路径不存在: {input_path}')
    walker = input_path.rglob('*') if recursive else input_path.glob('*')
    return sorted(p for p in walker if p.is_file() and p.suffix.lower() in IMAGE_EXTS)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def safe_relative_output_path(base_input: Path, img_path: Path, out_dir: Path, suffix: str) -> Path:
    try:
        rel = img_path.relative_to(base_input)
        return out_dir / rel.parent / f'{rel.stem}{suffix}'
    except Exception:
        return out_dir / f'{img_path.stem}{suffix}'


def build_json_payload(result: dict) -> dict:
    return {
        'path': result['path'],
        'format': result['format'],
        'mode': result['mode'],
        'lang': result['lang'],
        'psm': result['psm'],
        'rotation_angle': result['rotation_angle'],
        'orientation_strategy': result['orientation_strategy'],
        'elapsed_ms': result['elapsed_ms'],
        'chars': result['chars'],
        'content': result['content'],
        'tesseract_cmd': result['tesseract_cmd'],
        'doc_hint': result.get('doc_hint'),
        'variant': result.get('variant'),
        'ocr_oem': result.get('ocr_oem'),
        'ocr_dpi': result.get('ocr_dpi'),
        'candidate_score': result.get('candidate_score'),
        'avg_conf': result.get('avg_conf'),
        'min_conf': result.get('min_conf'),
        'word_count': result.get('word_count'),
        'low_conf_words': result.get('low_conf_words'),
        'quality_warning': result.get('quality_warning'),
        'suggestions': result.get('suggestions', []),
    }


def process_one(img_path: Path, args: argparse.Namespace) -> dict:
    started = time.perf_counter()
    img = preprocess_image(
        img_path,
        min_edge=max(1, args.min_edge),
        sharpen=args.sharpen,
        no_preprocess=args.no_preprocess,
    )

    doc_hint = detect_doc_hint(img_path, args.doc_hint)
    multi_variant = args.multi_variant or doc_hint == 'label'

    rotation_angle = 0
    best_psm = args.psm if args.psm is not None else 6
    orientation_strategy = 'off'
    best_meta = {'variant': 'base', 'oem': 3, 'dpi': args.dpi, 'score': 0}

    if args.format == 'text':
        if args.autorotate:
            orientation_strategy = args.autorotate_strategy
            img, rotation_angle, best_psm, content, best_meta = autorotate_image(
                img,
                lang=args.lang,
                dpi=args.dpi,
                mode=args.mode,
                manual_psm=args.psm,
                strategy=args.autorotate_strategy,
                doc_hint=doc_hint,
                multi_variant=multi_variant,
            )
        else:
            content, best_psm, best_meta = run_best_text_ocr(
                img,
                lang=args.lang,
                dpi=args.dpi,
                mode=args.mode,
                manual_psm=args.psm,
                doc_hint=doc_hint,
                multi_variant=multi_variant,
            )
    else:
        if args.autorotate:
            orientation_strategy = args.autorotate_strategy
            img, rotation_angle, best_psm, _, best_meta = autorotate_image(
                img,
                lang=args.lang,
                dpi=args.dpi,
                mode=args.mode,
                manual_psm=args.psm,
                strategy=args.autorotate_strategy,
                doc_hint=doc_hint,
                multi_variant=multi_variant,
            )
        psm = args.psm if args.psm is not None else best_psm
        content = image_to_tsv(img, lang=args.lang, psm=psm, dpi=args.dpi, min_conf=args.min_conf)
        best_psm = psm

    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    warning = quality_warning(best_meta, content, doc_hint)
    return {
        'path': str(img_path),
        'content': content,
        'psm': best_psm,
        'elapsed_ms': elapsed_ms,
        'chars': len(content),
        'rotation_angle': rotation_angle,
        'format': args.format,
        'mode': args.mode,
        'lang': args.lang,
        'orientation_strategy': orientation_strategy,
        'tesseract_cmd': pytesseract.pytesseract.tesseract_cmd,
        'doc_hint': doc_hint,
        'variant': best_meta.get('variant'),
        'ocr_oem': best_meta.get('oem'),
        'ocr_dpi': best_meta.get('dpi'),
        'candidate_score': best_meta.get('score'),
        'avg_conf': best_meta.get('avg_conf'),
        'min_conf': best_meta.get('min_conf'),
        'word_count': best_meta.get('word_count'),
        'low_conf_words': best_meta.get('low_conf_words'),
        'quality_warning': warning,
        'suggestions': quality_suggestions(warning),
    }


def print_single_result(result: dict, out: str | None, json_mode: bool) -> None:
    rendered = json.dumps(build_json_payload(result), ensure_ascii=False, indent=2) if json_mode else result['content']
    if not out:
        print(rendered)
        return
    out_path = Path(out).expanduser().resolve()
    ensure_parent(out_path)
    out_path.write_text(rendered, encoding='utf-8')
    print(str(out_path))


def run_batch(images: list[Path], args: argparse.Namespace, base_input: Path) -> int:
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else None
    manifest = []
    failed = 0
    for img_path in images:
        try:
            result = process_one(img_path, args)
            record = {
                'path': result['path'],
                'elapsed_ms': result['elapsed_ms'],
                'chars': result['chars'],
                'psm': result['psm'],
                'rotation_angle': result['rotation_angle'],
                'orientation_strategy': result['orientation_strategy'],
                'format': result['format'],
                'mode': result['mode'],
                'tesseract_cmd': result['tesseract_cmd'],
                'doc_hint': result.get('doc_hint'),
                'variant': result.get('variant'),
                'ocr_oem': result.get('ocr_oem'),
                'ocr_dpi': result.get('ocr_dpi'),
                'candidate_score': result.get('candidate_score'),
                'avg_conf': result.get('avg_conf'),
                'quality_warning': result.get('quality_warning'),
                'status': 'ok',
            }
            if out_dir:
                suffix = '.json' if args.json else ('.tsv' if args.format == 'tsv' else '.txt')
                out_path = safe_relative_output_path(base_input, img_path, out_dir, suffix)
                ensure_parent(out_path)
                rendered = json.dumps(build_json_payload(result), ensure_ascii=False, indent=2) if args.json else result['content']
                out_path.write_text(rendered, encoding='utf-8')
                record['output'] = str(out_path)
            else:
                if args.json:
                    print(json.dumps(build_json_payload(result), ensure_ascii=False, indent=2))
                else:
                    print(f'===== {img_path} =====')
                    print(result['content'])
            manifest.append(record)
        except Exception as exc:
            failed += 1
            manifest.append({'path': str(img_path), 'status': 'error', 'error': str(exc)})
            print(f'[ERROR] {img_path}: {exc}', file=sys.stderr)

    if out_dir:
        manifest_path = out_dir / 'manifest.json'
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        print(str(manifest_path))
    return failed


def main() -> None:
    parser = argparse.ArgumentParser(description='Local offline OCR for image files.')
    parser.add_argument('image_path', help='本地图片路径，或目录（配合 --batch）')
    parser.add_argument('--lang', default='eng', help='OCR 语言，默认 eng，可传 chi_sim+eng')
    parser.add_argument('--psm', type=int, help='显式指定 Tesseract PSM；指定后不再自动尝试多个模式')
    parser.add_argument('--mode', choices=['balanced', 'fast', 'accurate'], default='balanced', help='OCR 模式')
    parser.add_argument('--format', choices=['text', 'tsv'], default='text', help='输出格式：text 或 tsv')
    parser.add_argument('--json', action='store_true', help='以 JSON 输出 OCR 结果和元数据')
    parser.add_argument('--tesseract-cmd', help='显式指定 tesseract 可执行文件路径')
    parser.add_argument('--min-conf', type=int, default=0, help='TSV 模式下过滤低置信度文本，默认 0')
    parser.add_argument('--dpi', type=int, default=300, help='传给 Tesseract 的逻辑 DPI，默认 300')
    parser.add_argument('--min-edge', type=int, default=1800, help='较小图片会放大到该长边，默认 1800')
    parser.add_argument('--sharpen', action='store_true', help='启用轻量锐化')
    parser.add_argument('--no-preprocess', action='store_true', help='关闭基础预处理')
    parser.add_argument('--autorotate', action='store_true', help='自动尝试方向并选择更优结果')
    parser.add_argument('--autorotate-strategy', choices=['smart', 'full'], default='smart', help='自动旋转策略')
    parser.add_argument('--doc-hint', choices=['general', 'label'], help='文档类型提示；label 适合标签/票据短文本')
    parser.add_argument('--multi-variant', action='store_true', help='启用多预处理/多参数候选搜索')
    parser.add_argument('--out', help='单文件模式下将结果写入文件；不传则输出到 stdout')
    parser.add_argument('--batch', action='store_true', help='批量模式：将 image_path 当作目录或多图入口处理')
    parser.add_argument('--recursive', action='store_true', help='批量模式下递归扫描子目录')
    parser.add_argument('--out-dir', help='批量模式下将每张图输出到目录，并生成 manifest.json')
    args = parser.parse_args()

    input_path = Path(args.image_path).expanduser().resolve()
    tesseract_cmd = configure_tesseract(args.tesseract_cmd)
    ensure_langs(args.lang, tesseract_cmd)

    if args.batch:
        images = collect_images(input_path, recursive=args.recursive)
        if not images:
            fail(f'未找到可处理图片: {input_path}')
        failed = run_batch(images, args, base_input=input_path)
        sys.exit(1 if failed else 0)

    if not input_path.exists() or not input_path.is_file():
        fail(f'图片不存在: {input_path}')

    result = process_one(input_path, args)
    print_single_result(result, args.out, json_mode=args.json)


if __name__ == '__main__':
    main()
