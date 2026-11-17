"""Tests for sdef_parser against real macOS sdef files."""


class TestMusicSdef:
    def test_app_name(self, music_sdef_info):
        assert music_sdef_info.app_name == "Music"

    def test_has_music_suite_commands(self, music_sdef_info):
        music_cmds = [c for c in music_sdef_info.commands if c.suite_name == "Music Suite"]
        assert len(music_cmds) >= 18

    def test_standard_suite_commands_marked(self, music_sdef_info):
        std_cmds = [c for c in music_sdef_info.commands if c.is_standard_suite]
        std_names = {c.name for c in std_cmds}
        for expected in ("open", "close", "save", "print", "quit", "count",
                         "delete", "duplicate", "exists", "make", "move", "run"):
            assert expected in std_names, f"Expected '{expected}' in standard commands"

    def test_name_conversion(self, music_sdef_info):
        next_track = next(c for c in music_sdef_info.commands if c.name == "next track")
        assert next_track.cli_name == "next-track"
        assert next_track.func_name == "next_track"

    def test_sound_volume_is_rw(self, music_sdef_info):
        vol = next(p for p in music_sdef_info.properties
                   if p.name == "sound volume" and p.class_name == "application")
        assert vol.access == "rw"

    def test_player_state_is_read_only(self, music_sdef_info):
        ps = next(p for p in music_sdef_info.properties
                  if p.name == "player state" and p.class_name == "application")
        assert ps.access == "r"

    def test_enumerations_parsed(self, music_sdef_info):
        enum_names = {e.name for e in music_sdef_info.enumerations}
        assert "ePlS" in enum_names
        assert "eRpt" in enum_names
        assert "eShM" in enum_names

    def test_player_state_enum_values(self, music_sdef_info):
        epls = next(e for e in music_sdef_info.enumerations if e.name == "ePlS")
        value_names = [v[0] for v in epls.values]
        assert "stopped" in value_names
        assert "playing" in value_names
        assert "paused" in value_names

    def test_play_command_has_optional_direct_param(self, music_sdef_info):
        play = next(c for c in music_sdef_info.commands if c.name == "play")
        assert play.direct_parameter is not None
        assert play.direct_parameter.optional is True

    def test_play_command_has_once_param(self, music_sdef_info):
        play = next(c for c in music_sdef_info.commands if c.name == "play")
        once = next(p for p in play.parameters if p.name == "once")
        assert once.type == "boolean"
        assert once.optional is True

    def test_track_properties_exist(self, music_sdef_info):
        track_props = [p for p in music_sdef_info.properties if p.class_name == "track"]
        track_prop_names = {p.name for p in track_props}
        for expected in ("name", "artist", "album", "duration", "genre",
                         "rating", "played count", "favorited", "year"):
            assert expected in track_prop_names

    def test_add_command_direct_param_list_type(self, music_sdef_info):
        add = next(c for c in music_sdef_info.commands if c.name == "add")
        assert add.direct_parameter is not None
        assert "list" in add.direct_parameter.type


class TestCalendarSdef:
    def test_app_name(self, calendar_sdef_info):
        assert calendar_sdef_info.app_name == "Calendar"

    def test_non_hidden_non_standard_commands(self, calendar_sdef_info):
        visible = [c for c in calendar_sdef_info.commands
                   if not c.hidden and not c.is_standard_suite]
        names = {c.name for c in visible}
        assert "reload calendars" in names
        assert "switch view" in names
        assert "view calendar" in names
        assert "GetURL" in names
        assert "show" in names

    def test_hidden_commands_marked(self, calendar_sdef_info):
        hidden = [c for c in calendar_sdef_info.commands if c.hidden]
        hidden_names = {c.name for c in hidden}
        assert "create calendar" in hidden_names
        assert "make" in hidden_names
        assert "save" in hidden_names

    def test_class_extension_properties(self, calendar_sdef_info):
        cal_props = [p for p in calendar_sdef_info.properties if p.class_name == "calendar"]
        cal_names = {p.name for p in cal_props}
        assert "name" in cal_names
        assert "writable" in cal_names

    def test_enumerations(self, calendar_sdef_info):
        enum_names = {e.name for e in calendar_sdef_info.enumerations}
        assert "view type" in enum_names
        assert "participation status" in enum_names


class TestNameConversions:
    def test_multi_word_command(self, music_sdef_info):
        cmd = next(c for c in music_sdef_info.commands if c.name == "next track")
        assert cmd.cli_name == "next-track"
        assert cmd.func_name == "next_track"

    def test_single_word_command(self, music_sdef_info):
        cmd = next(c for c in music_sdef_info.commands if c.name == "pause")
        assert cmd.cli_name == "pause"
        assert cmd.func_name == "pause"
