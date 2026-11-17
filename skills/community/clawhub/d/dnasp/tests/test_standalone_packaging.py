"""Regression tests for the packaging of the dnasp skill.

These cover the reproducibility writers shipped beside dnasp.py, how dnasp.py
loads them, the report wording, the imports the skill relies on and the licence
travelling inside the skill directory.
"""
from pathlib import Path
import ast
import hashlib
import json
import os
import sys
import types

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dnasp as d

SKILL_DIR = Path(d.__file__).resolve().parent
SMALL_FASTA = '>a\nAAAT\n>b\nAATT\n>c\nAAAT\n>d\nATTT\n'


def _run(tmp_path, monkeypatch, name='run'):
    monkeypatch.setattr(d, 'HAS_MPL', False)
    source = tmp_path / f'{name}.fas'
    source.write_text(SMALL_FASTA, encoding='utf-8')
    out = tmp_path / f'{name}_out'
    code = d.main(['--input', str(source), '--output', str(out)])
    return code, out


def _assert_bundle(out):
    repro = out / 'reproducibility'
    for name in ('commands.sh', 'environment.yml', 'checksums.sha256', 'manifest.json'):
        assert (repro / name).is_file(), name


def test_bundle_survives_unrelated_module_named_reproducibility(tmp_path, monkeypatch):
    # An unrelated, already-imported module must not be picked up by the skill.
    monkeypatch.setitem(sys.modules, 'reproducibility', types.ModuleType('reproducibility'))
    code, out = _run(tmp_path, monkeypatch)
    assert code == 0
    _assert_bundle(out)


def test_bundle_ignores_conflicting_modules_earlier_on_sys_path(tmp_path, monkeypatch):
    decoy_dir = tmp_path / 'decoy'
    decoy_dir.mkdir()
    decoy = (
        'def _boom(*args, **kwargs):\n'
        '    raise RuntimeError("decoy writer used")\n'
        'write_commands_sh = write_environment_yml = write_checksums = _boom\n'
    )
    for module_name in ('reproducibility', '_repro_writers', '_dnasp_repro_writers'):
        (decoy_dir / f'{module_name}.py').write_text(decoy, encoding='utf-8')
        monkeypatch.delitem(sys.modules, module_name, raising=False)
    monkeypatch.syspath_prepend(str(decoy_dir))
    try:
        code, out = _run(tmp_path, monkeypatch)
    finally:
        # A decoy imported by a faulty loader must not leak into later tests.
        for module_name in ('reproducibility', '_repro_writers', '_dnasp_repro_writers'):
            module = sys.modules.get(module_name)
            if module is not None and str(decoy_dir) in str(getattr(module, '__file__', '')):
                del sys.modules[module_name]
    assert code == 0
    _assert_bundle(out)


def test_loading_writers_does_not_touch_sys_path_or_generic_module_names(tmp_path, monkeypatch):
    monkeypatch.delitem(sys.modules, 'reproducibility', raising=False)
    before = list(sys.path)
    code, _ = _run(tmp_path, monkeypatch)
    assert code == 0
    assert sys.path == before
    assert 'reproducibility' not in sys.modules


def test_checksums_verify_and_use_forward_slash_labels(tmp_path, monkeypatch):
    code, out = _run(tmp_path, monkeypatch)
    assert code == 0
    raw = (out / 'reproducibility' / 'checksums.sha256').read_bytes()
    assert b'\r' not in raw
    lines = raw.decode('utf-8').splitlines()
    assert lines
    labels = []
    for line in lines:
        digest, label = line.split('  ', 1)
        assert '\\' not in label
        assert hashlib.sha256((out / label).read_bytes()).hexdigest() == digest
        labels.append(label)
    assert 'reproducibility/manifest.json' in labels
    assert 'reproducibility/checksums.sha256' not in labels


def test_commands_sh_is_executable_lf_and_replays(tmp_path, monkeypatch):
    code, out = _run(tmp_path, monkeypatch)
    assert code == 0
    script = out / 'reproducibility' / 'commands.sh'
    raw = script.read_bytes()
    assert raw.startswith(b'#!/usr/bin/env bash\n')
    assert b'\r' not in raw
    if os.name != 'nt':
        assert os.access(script, os.X_OK)
    manifest = json.loads((out / 'reproducibility' / 'manifest.json').read_text(encoding='utf-8'))
    assert d.main(manifest['replay_arguments']) == 0


def test_environment_yml_records_python_and_packages(tmp_path, monkeypatch):
    code, out = _run(tmp_path, monkeypatch)
    assert code == 0
    text = (out / 'reproducibility' / 'environment.yml').read_text(encoding='utf-8')
    assert text.startswith('name: dnasp\n')
    assert '  - conda-forge\n' in text
    python_line = [line for line in text.splitlines() if line.startswith('  - python=')]
    assert python_line == [f'  - python={d.platform.python_version()}']
    manifest = json.loads((out / 'reproducibility' / 'manifest.json').read_text(encoding='utf-8'))
    for name, version in manifest['packages'].items():
        assert f'      - {name}=={version}\n' in text


def test_licence_ships_inside_the_skill_directory():
    licence = SKILL_DIR / 'LICENSE.txt'
    assert licence.is_file()
    text = licence.read_text(encoding='utf-8')
    assert text.startswith('MIT License')
    assert 'David de Lorenzo' in text


def test_skill_imports_only_the_standard_library_matplotlib_and_its_own_modules():
    allowed = set(sys.stdlib_module_names) | {'matplotlib'} | {p.stem for p in SKILL_DIR.glob('*.py')}
    for path in SKILL_DIR.glob('*.py'):
        tree = ast.parse(path.read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots = [alias.name.split('.')[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                roots = [node.module.split('.')[0]]
            else:
                continue
            for root in roots:
                assert root in allowed, f'{path.name}:{node.lineno} imports {root}'


def test_report_names_dnasp_python_and_keeps_the_disclaimer(tmp_path, monkeypatch):
    code, out = _run(tmp_path, monkeypatch)
    assert code == 0
    report = (out / 'report.md').read_text(encoding='utf-8')
    assert '**Tool**: DnaSP-Python  \n' in report
    assert 'Statistics computed using DnaSP-Python, reimplementing' in report
    assert 'DnaSP-Python is a research and educational tool. It is not a medical device' in report
