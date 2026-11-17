"""Offline tests for classic-ir."""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
IR = os.path.join(HERE, '..', 'ir.py')


def run(*args):
    r = subprocess.run([sys.executable, IR] + list(args),
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout


def test_index_search_expand_fuse():
    tmp = tempfile.mkdtemp()
    open(os.path.join(tmp, 'a.md'), 'w').write(
        '# BM25 retrieval\nBM25 ranks documents by term saturation.')
    open(os.path.join(tmp, 'b.md'), 'w').write(
        '# Dense embeddings\nVector search over learned representations.')
    db = os.path.join(tmp, 'c.db')
    out = run('index', tmp, '--db', db)
    assert 'indexed 2 files' in out, out
    res = json.loads(run('search', db, 'BM25 term saturation'))
    assert res and res[0]['path'].endswith('a.md'), res
    exp = json.loads(run('expand', db, 'BM25'))
    assert isinstance(exp, list), exp
    ra = os.path.join(tmp, 'ra.json')
    rb = os.path.join(tmp, 'rb.json')
    run('search', db, 'BM25', '--out', ra)
    run('search', db, 'embeddings', '--out', rb)
    fused = json.loads(run('fuse', ra, rb))
    assert len(fused) == 2, fused
    print('test_index_search_expand_fuse PASS')


if __name__ == '__main__':
    test_index_search_expand_fuse()
