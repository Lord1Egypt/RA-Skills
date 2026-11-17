#!/usr/bin/env python3
"""
Tests for the schema registry (ROADMAP T1.1).

The registry is the one place that inspects Photos.sqlite's schema, so a
renamed column becomes a one-line change in LOGICAL_COLUMNS.
"""

import re
import sqlite3
from pathlib import Path

import pytest

from _common import PhotosDB, connect_db, detect_face_schema, format_degraded, has_timezone_offset, require_uuid_support
from _schema import (
    LOGICAL_COLUMNS,
    Degradation,
    PhotosConnection,
    SchemaRegistry,
    SchemaUnsupportedError,
    album_junction,
    get_schema,
)

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"


def make_db(*ddl: str) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    for statement in ddl:
        conn.execute(statement)
    return conn


OLD_FACE = "CREATE TABLE ZDETECTEDFACE (Z_PK INTEGER PRIMARY KEY, ZPERSON INTEGER, ZASSET INTEGER)"
NEW_FACE = "CREATE TABLE ZDETECTEDFACE (Z_PK INTEGER PRIMARY KEY, ZPERSONFORFACE INTEGER, ZASSETFORFACE INTEGER)"


class TestSchemaRegistry:
    def test_tables_and_columns(self):
        schema = SchemaRegistry(make_db("CREATE TABLE ZASSET (Z_PK INTEGER, ZUUID TEXT)", "CREATE TABLE ZB (x)"))
        assert schema.tables() == ("ZASSET", "ZB")
        assert schema.columns("ZASSET") == {"Z_PK", "ZUUID"}
        assert schema.has_column("ZASSET", "ZUUID")
        assert not schema.has_column("ZASSET", "ZNOPE")

    def test_missing_table_has_no_columns(self):
        schema = SchemaRegistry(make_db())
        assert not schema.has_table("ZDETECTEDFACE")
        assert schema.columns("ZDETECTEDFACE") == frozenset()
        assert schema.col("face.person_fk") is None

    def test_table_names_are_quoted(self):
        schema = SchemaRegistry(make_db('CREATE TABLE "odd ""name""" (a)'))
        assert schema.columns('odd "name"') == {"a"}

    @pytest.mark.parametrize(
        ("ddl", "person", "asset"),
        [(OLD_FACE, "ZPERSON", "ZASSET"), (NEW_FACE, "ZPERSONFORFACE", "ZASSETFORFACE")],
    )
    def test_logical_names_resolve_per_schema(self, ddl, person, asset):
        schema = SchemaRegistry(make_db(ddl))
        assert schema.col("face.person_fk") == person
        assert schema.col("face.asset_fk") == asset

    def test_preferred_candidate_wins_when_both_exist(self):
        both = "CREATE TABLE ZDETECTEDFACE (ZPERSON INTEGER, ZPERSONFORFACE INTEGER)"
        assert SchemaRegistry(make_db(both)).col("face.person_fk") == "ZPERSONFORFACE"

    def test_require_names_every_missing_column(self):
        schema = SchemaRegistry(make_db("CREATE TABLE ZASSET (Z_PK INTEGER)"))
        with pytest.raises(SchemaUnsupportedError, match=r"ZASSET\.ZUUID.*ZDETECTEDFACE\.ZQUALITYMEASURE"):
            schema.require("asset.uuid", "face.quality", operation="Test")

    def test_unknown_logical_name_is_a_programming_error(self):
        with pytest.raises(KeyError):
            SchemaRegistry(make_db()).has("asset.typo")

    @pytest.mark.parametrize("logical", sorted(LOGICAL_COLUMNS))
    def test_logical_map_is_well_formed(self, logical):
        table, candidates = LOGICAL_COLUMNS[logical]
        assert re.fullmatch(r"Z[A-Z_0-9]+", table)
        assert candidates
        assert all(re.fullmatch(r"Z[A-Z_0-9]+", name) for name in candidates)


class TestCaching:
    def test_connect_db_caches_one_registry(self, tmp_path):
        path = tmp_path / "Photos.sqlite"
        make_db("CREATE TABLE ZASSET (Z_PK INTEGER)").backup(sqlite3.connect(path))
        conn = connect_db(str(path))
        assert isinstance(conn, PhotosConnection)
        assert get_schema(conn) is get_schema(conn.cursor())
        conn.close()

    def test_plain_connections_still_work(self):
        conn = make_db("CREATE TABLE ZASSET (Z_PK INTEGER, ZUUID TEXT)")
        assert get_schema(conn).has("asset.uuid")
        assert get_schema(conn.cursor()).has("asset.uuid")


class TestCommonWrappers:
    """The pre-registry helpers keep their signatures and behaviour."""

    def test_detect_face_schema(self):
        assert detect_face_schema(make_db(NEW_FACE).cursor()) == {
            "person_fk": "ZPERSONFORFACE",
            "asset_fk": "ZASSETFORFACE",
        }
        assert detect_face_schema(make_db(OLD_FACE).cursor()) == {"person_fk": "ZPERSON", "asset_fk": "ZASSET"}
        assert detect_face_schema(make_db().cursor()) == {"person_fk": "ZPERSON", "asset_fk": "ZASSET"}

    def test_has_timezone_offset(self):
        with_tz = make_db("CREATE TABLE ZADDITIONALASSETATTRIBUTES (ZASSET INTEGER, ZTIMEZONEOFFSET INTEGER)")
        assert has_timezone_offset(with_tz.cursor())
        assert not has_timezone_offset(make_db("CREATE TABLE ZADDITIONALASSETATTRIBUTES (ZASSET INTEGER)").cursor())

    def test_require_uuid_support(self):
        require_uuid_support(make_db("CREATE TABLE ZASSET (ZUUID TEXT)").cursor(), "Cleanup")
        with pytest.raises(SchemaUnsupportedError, match="ZUUID"):
            require_uuid_support(make_db("CREATE TABLE ZASSET (Z_PK INTEGER)").cursor(), "Cleanup")


@pytest.mark.parametrize("script", sorted(p.name for p in SCRIPTS_DIR.glob("*.py") if p.name != "_schema.py"))
def test_only_the_registry_inspects_the_schema(script):
    source = (SCRIPTS_DIR / script).read_text(encoding="utf-8")
    probes = re.findall(r"PRAGMA\s+table_info|pragma_table_info\(|FROM\s+sqlite_master", source, re.IGNORECASE)
    assert not probes, f"{script} inspects the schema directly; use _schema.get_schema() instead"


class TestDegradationHelpers:
    def test_physical_names_resolve(self):
        schema = SchemaRegistry(make_db("CREATE TABLE ZASSET (ZKIND INTEGER)"))
        assert schema.has("ZASSET.ZKIND")
        assert not schema.has("ZASSET.ZNOPE")
        assert schema.missing("ZASSET.ZKIND", "ZASSET.ZNOPE", "face.person_fk") == [
            "ZASSET.ZNOPE",
            "ZDETECTEDFACE.ZPERSONFORFACE/ZPERSON",
        ]

    def test_select_degrades_to_null(self):
        schema = SchemaRegistry(make_db("CREATE TABLE ZPERSON (Z_PK INTEGER, ZFULLNAME TEXT)"))
        assert schema.select("ZPERSON.ZFULLNAME", "p") == "p.ZFULLNAME"
        assert schema.select("ZPERSON.ZFACECOUNT", "p") == "NULL AS ZFACECOUNT"
        assert schema.select("ZPERSON.ZFACECOUNT", "p", as_="n") == "NULL AS n"
        assert schema.select("ZPERSON.ZFULLNAME", "p", as_="name") == "p.ZFULLNAME AS name"

    def test_degradation_records_each_section_once(self):
        degraded = Degradation(SchemaRegistry(make_db("CREATE TABLE ZASSET (ZKIND INTEGER)")))
        assert degraded.check("kinds", "ZASSET.ZKIND")
        assert not degraded.check("bursts", "ZASSET.ZAVALANCHEKIND", "ZASSET.ZAVALANCHEPICKTYPE")
        assert not degraded.check("bursts", "ZASSET.ZAVALANCHEKIND")
        assert degraded.entries == [
            {"section": "bursts", "reason": "missing column(s): ZASSET.ZAVALANCHEKIND, ZASSET.ZAVALANCHEPICKTYPE"}
        ]

    @pytest.mark.parametrize("number", [26, 27, 28, 33])
    def test_album_junction_is_found_by_shape(self, number):
        schema = SchemaRegistry(make_db(f"CREATE TABLE Z_{number}ASSETS (Z_{number}ALBUMS INTEGER, Z_3ASSETS INTEGER)"))
        assert album_junction(schema) == (f"Z_{number}ASSETS", f"Z_{number}ALBUMS", "Z_3ASSETS")

    def test_no_album_junction(self):
        assert album_junction(SchemaRegistry(make_db("CREATE TABLE Z_1KEYWORDS (a)"))) is None

    def test_format_degraded(self):
        assert format_degraded({"degraded": []}) == ""
        note = format_degraded({"degraded": [{"section": "bursts", "reason": "missing column(s): ZASSET.ZX"}]})
        assert "bursts: missing column(s): ZASSET.ZX" in note


def test_photosdb_require_closes_and_raises(tmp_path):
    path = tmp_path / "Photos.sqlite"
    make_db("CREATE TABLE ZASSET (Z_PK INTEGER)").backup(sqlite3.connect(path))
    with (
        pytest.raises(SchemaUnsupportedError, match=r"ZASSET\.ZKIND.*Test op"),
        PhotosDB(str(path), require=("ZASSET.ZKIND",), operation="Test op"),
    ):
        pass


class TestVirtualTables:
    """Photos keeps an R*Tree (Z_RT_Asset_boundedByRect). Connecting to it prepares the module's own
    INSERTs, which the read-only authorizer refuses, so the registry must never touch it."""

    RTREE = "CREATE VIRTUAL TABLE Z_RT_Asset_boundedByRect USING rtree(Z_PK, ZMINX, ZMAXX, ZMINY, ZMAXY)"

    @pytest.fixture
    def guarded_conn(self, tmp_path):
        path = tmp_path / "Photos.sqlite"
        make_db("CREATE TABLE ZASSET (Z_PK INTEGER, ZKIND INTEGER)", self.RTREE).backup(sqlite3.connect(path))
        conn = connect_db(str(path))
        yield conn
        conn.close()

    def test_connecting_to_the_rtree_is_what_the_guard_refuses(self, guarded_conn):
        with pytest.raises(sqlite3.DatabaseError, match="not authorized"):
            guarded_conn.execute('PRAGMA table_info("Z_RT_Asset_boundedByRect")').fetchall()

    def test_registry_never_connects_to_virtual_tables(self, guarded_conn):
        schema = SchemaRegistry(guarded_conn)
        assert schema.is_virtual("Z_RT_Asset_boundedByRect")
        assert schema.columns("Z_RT_Asset_boundedByRect") == frozenset()
        assert schema.columns("Z_RT_Asset_boundedByRect_node")  # its shadow tables are ordinary tables
        assert len(schema.fingerprint()) == 64

    def test_fingerprint_includes_virtual_tables(self):
        without = SchemaRegistry(make_db("CREATE TABLE ZASSET (Z_PK INTEGER)")).fingerprint()
        with_rtree = SchemaRegistry(make_db("CREATE TABLE ZASSET (Z_PK INTEGER)", self.RTREE)).fingerprint()
        assert without != with_rtree
