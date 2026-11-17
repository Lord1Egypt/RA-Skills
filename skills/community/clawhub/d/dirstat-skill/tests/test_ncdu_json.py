from pathlib import Path

from dirstat_skill.ncdu_json import parse_ncdu_export


def test_parse_ncdu_export_flattens_directory_tree() -> None:
    fixture = Path("tests/fixtures/ncdu_minimal_export.json")

    result = parse_ncdu_export(fixture)

    assert result.root_path == "/sample"
    assert len(result.nodes) == 4
    assert result.nodes[0].path == "/sample"
    assert result.nodes[0].is_dir is True
    assert result.nodes[0].dsize == 3221241856
    assert result.nodes[1].path == "/sample/cache"
    assert result.nodes[1].is_dir is True
    assert result.nodes[1].dsize == 3221233664
    assert result.nodes[2].path == "/sample/cache/huge.log"
    assert result.nodes[2].is_dir is False
    assert result.nodes[2].dsize == 3221225472

