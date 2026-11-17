"""Workspace-isolated LibreOffice adapter, reusing renderer discovery and rasterization.

Auto deliberately selects LibreOffice only: GUI Office automation cannot promise a
workspace-local profile. No shell, user scripts, or renderer options are accepted.
"""
from __future__ import annotations
import os
from pathlib import Path
import subprocess
import time
from ppt_qa.render_report import build_render_report, iso_now
from ppt_qa.renderers.base import RenderResult, elapsed_since
from ppt_qa.renderers.libreoffice import LibreOfficeRenderer
from ppt_qa.renderers.pdf_tools import rasterize_pdf_to_pngs


def run_render_report(pptx_path, output_dir, *, engine='auto', expected_slides=None,
                      expected_aspect, timeout=300, dpi=144):
    started = time.monotonic(); started_at = iso_now()
    base = LibreOfficeRenderer()
    disabled = os.environ.get('PPTSMITH_TEST_RENDERER_UNAVAILABLE') == '1' or os.environ.get('PPTSMITH_TEST_RENDERERS') == 'none'
    soffice = None if disabled else base._soffice_path()
    if soffice is None:
        result = RenderResult('unavailable', None, None, None, errors=['RENDER_ENGINE_UNAVAILABLE'])
    else:
        output_dir.mkdir(parents=True, exist_ok=False)
        profile = output_dir / 'profile'; profile.mkdir()
        home = output_dir / 'home'; home.mkdir()
        tmp = output_dir / 'tmp'; tmp.mkdir()
        env = dict(os.environ)
        env.update(HOME=str(home), TMPDIR=str(tmp), TMP=str(tmp), TEMP=str(tmp),
                   XDG_CONFIG_HOME=str(home / '.config'), XDG_CACHE_HOME=str(home / '.cache'),
                   XDG_DATA_HOME=str(home / '.local' / 'share'))
        command = [soffice, '-env:UserInstallation=' + profile.as_uri(), '--headless',
                   '--convert-to', 'pdf', '--outdir', str(output_dir), str(pptx_path)]
        errors = []; logs = []; images = []; target = output_dir / 'deck.pdf'
        try:
            completed = subprocess.run(command, env=env, text=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, timeout=timeout, check=False)
            (output_dir / 'stdout.log').write_text(completed.stdout, encoding='utf-8')
            (output_dir / 'stderr.log').write_text(completed.stderr, encoding='utf-8')
            if completed.returncode: errors.append('RENDER_EXPORT_FAILED')
            produced = output_dir / (pptx_path.stem + '.pdf')
            if produced.is_file(): produced.replace(target)
            else: errors.append('RENDER_PDF_MISSING')
            if target.is_file():
                images, logs = rasterize_pdf_to_pngs(target, output_dir / 'slides', dpi=dpi, timeout_seconds=timeout)
        except subprocess.TimeoutExpired:
            errors.append('RENDER_TIMEOUT')
        # Version discovery is informational and must use the same private profile.
        version = None
        try:
            v = subprocess.run([soffice, '-env:UserInstallation=' + profile.as_uri(), '--version'],
                               env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               timeout=10, check=False)
            version = v.stdout.strip() or None
        except (OSError, subprocess.TimeoutExpired): pass
        result = RenderResult('passed' if images and not errors else 'failed', 'libreoffice', version,
                              target if target.is_file() else None, images, logs, errors,
                              elapsed_since(started), len(images))
    return build_render_report(pptx_path, result, started_at=started_at,
                               expected_slides=expected_slides, expected_aspect=expected_aspect)
