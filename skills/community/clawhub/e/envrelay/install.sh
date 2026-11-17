#!/bin/sh
# Install EnvRelay: the envrelay binary and the EnvRelay skill, in one command.
#
# Every release carries this file as install.sh, and the one-line command,
#   curl -fsSL https://envrelay.com/install.sh | sh
# runs the latest release's copy, which the site redirects to. The same file
# ships inside the skill, so an agent that has the skill but not the binary
# runs `sh <skill dir>/install.sh --bin-only` once the user says yes.
# In order, it:
#
#   1. downloads SHA256SUMS, the envrelay binary for this machine and the skill
#      from one release on GitHub, over HTTPS, and refuses any file whose
#      checksum does not match;
#   2. puts envrelay in ~/.local/bin (or --bin-dir), replacing it atomically;
#   3. puts the skill in ~/.agents/skills/envrelay, which Codex, Cursor, Gemini
#      CLI, OpenCode, Copilot and most other agents read, and symlinks it into
#      ~/.claude/skills (and ~/.kiro/skills, ~/.cline/skills when present);
#   4. adds the bin directory to PATH in your shell's rc file if it is missing;
#   5. checks for python3 3.9+ and git 2.31+, which the skill's scripts use.
#
# It never uses sudo, never touches a backup, and never replaces a skill
# directory or link it did not create. Why it exists, and why it is not one of
# the skill's scripts: docs/decisions/024-one-command-install.md.
#
# Everything is a function until the last line, so a download cut off halfway
# runs nothing.

set -eu
umask 022

REPO=FutrixDev/envrelay-skill
MARKER=.envrelay-installer
PATH_COMMENT='# Added by the EnvRelay installer'
# Read here, not in a function: zsh sets $0 to the function's name there.
SELF=$0

usage() {
	cat <<'EOF'
Install EnvRelay: the envrelay binary and the EnvRelay skill for coding agents.

  sh install.sh [OPTIONS]

Every release carries this file as install.sh; envrelay.com redirects to the
latest release's copy. Through the one-line command, options go after sh -s --:

  curl -fsSL https://envrelay.com/install.sh | sh -s -- --dry-run

Options:
  --version X.Y.Z    install that release instead of the latest one
  --bin-dir DIR      where envrelay goes (default ~/.local/bin, or $ENVRELAY_BIN_DIR)
  --bin-only         install the binary only, not the skill
  --no-modify-path   never edit a shell rc file
  --dry-run          say what would happen; download and change nothing
  --uninstall        remove what this installer put in place (never a backup)
  -h, --help         show this help

Run from inside an installed skill (sh <skill dir>/install.sh), it installs the
release that matches that skill's version rather than the latest one. Every
download comes from https://github.com/FutrixDev/envrelay-skill/releases.
EOF
}

say() { printf '%s\n' "$*"; }
die() {
	printf 'error: %s\n' "$*" >&2
	exit 1
}
have() { command -v "$1" >/dev/null 2>&1; }
# Notes are collected and printed after the work, where they will be read.
note() {
	notes="$notes${notes:+
}$*"
}
print_notes() {
	[ -n "$notes" ] || return 0
	say ""
	printf '%s\n' "$notes" | while IFS= read -r line; do say "  * $line"; done
}

cleanup() {
	[ -z "$tmp" ] || rm -rf "$tmp"
	[ -z "$staged_bin" ] || rm -f "$staged_bin"
	[ -z "$staged_skill" ] || rm -rf "$staged_skill"
	# Stopped between moving the previous skill aside and putting the new one
	# in its place: put the previous one back.
	if [ -n "$old_skill" ] && [ -d "$old_skill" ]; then
		if [ -e "$canonical" ] || [ -L "$canonical" ]; then
			rm -rf "$old_skill"
		else
			mv "$old_skill" "$canonical"
		fi
	fi
}

# The version in the frontmatter of the SKILL.md next to this script, when it
# runs from inside an installed skill; nothing when it is piped from curl.
# It is metadata.version at whatever indentation the file has: gh skill install
# rewrites the frontmatter with sorted keys and four spaces.
skill_version() {
	case $SELF in
	*/install.sh) dir=${SELF%/*} ;;
	install.sh) dir=. ;;
	*) return 0 ;;
	esac
	[ -f "$dir/SKILL.md" ] || return 0
	awk 'NR == 1 && $0 != "---" { exit }
		NR > 1 && $0 == "---" { exit }
		/^[ \t]*#/ || /^[ \t]*$/ { next }
		/^[^ \t]/ { inmeta = ($0 ~ /^metadata:[ \t]*(#.*)?$/); depth = 0; next }
		!inmeta { next }
		{ match($0, /^[ \t]+/); if (!depth) depth = RLENGTH }
		RLENGTH == depth && $1 == "version:" { v = $2; gsub(/["'\'']/, "", v); print v; exit }' "$dir/SKILL.md"
}

detect_platform() {
	os=$(uname -s)
	arch=$(uname -m)
	case $os in
	Darwin)
		asset=universal-apple-darwin
		platform="macOS ($arch)"
		;;
	Linux)
		case $arch in
		x86_64 | amd64) asset=x86_64-unknown-linux-musl ;;
		aarch64 | arm64) asset=aarch64-unknown-linux-musl ;;
		*) die "there is no prebuilt envrelay for Linux on $arch; build it from source: https://github.com/$REPO" ;;
		esac
		platform="Linux ($arch)"
		;;
	*) die "EnvRelay runs on macOS and Linux, not $os (on Windows, use WSL)" ;;
	esac
}

resolve_paths() {
	[ -n "$bin_dir" ] || bin_dir=$HOME/.local/bin
	case $bin_dir in
	\~) bin_dir=$HOME ;;
	\~/*) bin_dir=$HOME/${bin_dir#\~/} ;;
	esac
	case $bin_dir in
	/*) ;;
	*) bin_dir=$(pwd)/$bin_dir ;;
	esac
	while [ "$bin_dir" != / ] && [ "${bin_dir%/}" != "$bin_dir" ]; do bin_dir=${bin_dir%/}; done
	# The directory is written into a shell rc file inside double quotes.
	case $bin_dir in
	*'"'* | *'$'* | *'`'* | *\\*) die "--bin-dir may not contain quotes, \$, backticks or backslashes: $bin_dir" ;;
	esac
	skills_root=$HOME/.agents/skills
	canonical=$skills_root/envrelay
	claude_skills=${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills
}

# Agents that do not read ~/.agents/skills get a symlink to it: Claude Code
# always, since the skill is written for it first; Kiro and Cline when present.
each_link_dir() {
	"$@" "$claude_skills"
	if [ -d "$HOME/.kiro" ]; then "$@" "$HOME/.kiro/skills"; fi
	if [ -d "$HOME/.cline" ]; then "$@" "$HOME/.cline/skills"; fi
}

same_dir() {
	[ -d "$1" ] && [ -d "$2" ] &&
		[ "$(CDPATH='' cd -P "$1" && pwd)" = "$(CDPATH='' cd -P "$2" && pwd)" ]
}

# absent | ours (a directory this installer made) | theirs (anything else)
skill_state() {
	if [ -L "$canonical" ]; then
		echo theirs
	elif [ -d "$canonical" ] && [ -f "$canonical/$MARKER" ]; then
		echo ours
	elif [ -e "$canonical" ]; then
		echo theirs
	else
		echo absent
	fi
}

# absent | linked (points at the installed skill, whoever made it) | taken
link_state() {
	if [ -L "$1/envrelay" ]; then
		if [ "$(readlink "$1/envrelay")" = "$canonical" ] || same_dir "$1/envrelay" "$canonical"; then
			echo linked
		else
			echo taken
		fi
	elif [ -e "$1/envrelay" ]; then
		echo taken
	else
		echo absent
	fi
}

link_one() {
	case $(link_state "$1") in
	linked) say "    $1/envrelay already points at it" ;;
	taken) note "left $1/envrelay as it is: this installer did not make it. Remove it and run the installer again to link the installed skill there." ;;
	absent)
		if [ "$dry_run" = 1 ]; then
			say "    would link $1/envrelay -> $canonical"
			return
		fi
		mkdir -p "$1" || die "could not create $1"
		ln -s "$canonical" "$1/envrelay" || die "could not create $1/envrelay"
		say "    linked $1/envrelay"
		;;
	esac
}

unlink_one() {
	[ "$(link_state "$1")" = linked ] || return 0
	if [ "$dry_run" = 1 ]; then
		say "    would remove $1/envrelay"
	else
		rm -f "$1/envrelay"
		say "    removed $1/envrelay"
	fi
}

fetch() {
	if have curl; then
		curl --proto '=https' --tlsv1.2 -fsSL --retry 3 -o "$2" "$1"
	elif have wget; then
		wget -q -O "$2" "$1"
	else
		die "downloading EnvRelay needs curl or wget"
	fi || die "could not download $1 (is there a published release? --version picks one)"
}

verify() {
	want=$(awk -v n="$2" '$2 == n || $2 == "*" n { print $1; exit }' "$tmp/SHA256SUMS")
	[ -n "$want" ] || die "SHA256SUMS has no entry for $2"
	if have sha256sum; then
		got=$(sha256sum "$1")
	elif have shasum; then
		got=$(shasum -a 256 "$1")
	elif have openssl; then
		got=$(openssl dgst -sha256 -r "$1")
	else
		die "checking the download needs sha256sum, shasum or openssl"
	fi
	got=${got%% *}
	[ "$got" = "$want" ] ||
		die "$2 does not match SHA256SUMS, so it was not installed. If a new release came out while this ran, run the installer again."
}

version_note() {
	[ -x "$bin_dir/envrelay" ] || return 0
	current=$("$bin_dir/envrelay" --version </dev/null 2>/dev/null || true)
	printf ' (replacing %s)' "${current:-an envrelay that does not report its version}"
}

install_binary() {
	src=$tmp/bin/envrelay-$asset/envrelay
	[ -f "$src" ] || die "envrelay-$asset.tar.gz has no envrelay-$asset/envrelay in it"
	[ ! -d "$bin_dir/envrelay" ] || die "$bin_dir/envrelay is a directory"
	mkdir -p "$bin_dir" || die "could not create $bin_dir"
	staged_bin=$bin_dir/.envrelay.new.$$
	cp "$src" "$staged_bin" || die "could not write to $bin_dir"
	chmod 755 "$staged_bin"
	# Run it where it will live: /tmp is mounted noexec on some systems.
	installed_version=$("$staged_bin" --version </dev/null 2>&1) ||
		die "the downloaded envrelay does not run on this machine: $installed_version"
	case $installed_version in
	"envrelay "*) ;;
	*) die "the downloaded envrelay printed something unexpected: $installed_version" ;;
	esac
	mv -f "$staged_bin" "$bin_dir/envrelay" || die "could not replace $bin_dir/envrelay"
	say "    $installed_version -> $bin_dir/envrelay"
}

install_skill() {
	if [ "$(skill_state)" = theirs ]; then
		note "left $canonical as it is: another tool (npx skills, a copy, a link) put it there. Update it with that tool, or remove it and run the installer again."
		return
	fi
	[ -f "$tmp/skill/envrelay/SKILL.md" ] || die "envrelay-skill.tar.gz has no envrelay/SKILL.md in it"
	mkdir -p "$skills_root" || die "could not create $skills_root"
	# Staged beside skills/, not in it, so no agent ever sees a half-made copy.
	staged_skill=$HOME/.agents/.envrelay-skill.new.$$
	rm -rf "$staged_skill"
	mv "$tmp/skill/envrelay" "$staged_skill" || die "could not stage the skill in $HOME/.agents"
	say "Installed by EnvRelay's install.sh. Running it again replaces this directory; install.sh --uninstall removes it." >"$staged_skill/$MARKER"
	if [ -d "$canonical" ]; then
		old_skill=$HOME/.agents/.envrelay-skill.old.$$
		mv "$canonical" "$old_skill" || die "could not move the previous skill aside"
	fi
	mv "$staged_skill" "$canonical" || die "could not install the skill in $canonical"
	if [ -n "$old_skill" ]; then
		rm -rf "$old_skill"
		old_skill=''
	fi
	say "    skill -> $canonical"
	each_link_dir link_one
}

plan_skill() {
	case $(skill_state) in
	theirs)
		say "    would leave $canonical as it is"
		note "$canonical was put there by another tool (npx skills, a copy, a link); the installer leaves it alone."
		return
		;;
	ours) say "    would replace $canonical (from an earlier run)" ;;
	absent) say "    would install the skill in $canonical" ;;
	esac
	each_link_dir link_one
}

path_has() {
	case ":${PATH:-}:" in
	*":$1:"*) return 0 ;;
	*) return 1 ;;
	esac
}

pick_rc() {
	case ${SHELL:-sh} in
	zsh | */zsh) rc=${ZDOTDIR:-$HOME}/.zshrc ;;
	bash | */bash)
		if [ "$os" = Darwin ]; then
			# Terminal windows on macOS are login shells: first of these wins.
			rc=$HOME/.bash_profile
			for f in "$HOME/.bash_profile" "$HOME/.bash_login" "$HOME/.profile"; do
				if [ -f "$f" ]; then
					rc=$f
					break
				fi
			done
		else
			rc=$HOME/.bashrc
		fi
		;;
	fish | */fish) rc=${XDG_CONFIG_HOME:-$HOME/.config}/fish/conf.d/envrelay.fish ;;
	*) rc=$HOME/.profile ;;
	esac
	case $rc in
	*.fish) rc_line="contains -- \"$bin_dir\" \$PATH; or set -gx PATH \"$bin_dir\" \$PATH" ;;
	*) rc_line="export PATH=\"$bin_dir:\$PATH\"" ;;
	esac
}

setup_path() {
	if path_has "$bin_dir"; then
		[ "$dry_run" = 0 ] || say "    $bin_dir is already on PATH"
		return
	fi
	pick_rc
	if [ "$modify_path" = 0 ]; then
		note "$bin_dir is not on your PATH. Add it, or run envrelay as $bin_dir/envrelay."
		return
	fi
	if [ -f "$rc" ] && grep -Fqx "$rc_line" "$rc"; then
		note "$rc already puts $bin_dir on PATH; a new terminal picks it up."
		return
	fi
	if [ "$dry_run" = 1 ]; then
		say "    would add $bin_dir to PATH in $rc"
		return
	fi
	mkdir -p "${rc%/*}"
	printf '\n%s\n%s\n' "$PATH_COMMENT" "$rc_line" >>"$rc" || die "could not write $rc"
	say "    added $bin_dir to PATH in $rc"
	note "open a new terminal so that envrelay is on its PATH (until then: $bin_dir/envrelay)."
}

check_shadowing() {
	path_has "$bin_dir" || return 0
	first=$(command -v envrelay 2>/dev/null || true)
	if [ -z "$first" ] || [ "$first" = "$bin_dir/envrelay" ]; then return 0; fi
	note "$first comes before $bin_dir on your PATH, so plain \`envrelay\` runs that one. Remove it, or put $bin_dir first."
}

check_tools() {
	# On a Mac without the Command Line Tools, /usr/bin/python3 and /usr/bin/git
	# are stubs that only offer to install them.
	if [ "$os" = Darwin ] && ! xcode-select -p >/dev/null 2>&1; then
		py=$(command -v python3 || true)
		gt=$(command -v git || true)
		if [ -z "$py" ] || [ "$py" = /usr/bin/python3 ] || [ -z "$gt" ] || [ "$gt" = /usr/bin/git ]; then
			if [ "$dry_run" = 1 ]; then
				say "    would open Apple's installer for the Command Line Tools (python3 and git come with them)"
			else
				xcode-select --install >/dev/null 2>&1 || true
				note "python3 and git come with Apple's Command Line Tools, which this Mac does not have yet. Click Install in the window that opened and let it finish; nothing else is needed. No window? Run: xcode-select --install"
			fi
			return
		fi
	fi
	missing=''
	if ! have python3; then
		missing=python3
	elif ! PYTHONDONTWRITEBYTECODE=1 python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))' </dev/null >/dev/null 2>&1; then
		missing="python3 3.9 or newer (this one is $(python3 --version 2>&1 </dev/null))"
	fi
	if ! have git; then
		missing="${missing:+$missing and }git"
	elif ! git --version </dev/null 2>/dev/null | awk '{ split($3, v, "."); ok = v[1] + 0 > 2 || (v[1] + 0 == 2 && v[2] + 0 >= 31) } END { exit !ok }'; then
		# git_classify.py hands git its settings in GIT_CONFIG_COUNT (ADR-028).
		missing="${missing:+$missing and }git 2.31 or newer (this one is $(git --version 2>&1 </dev/null))"
	fi
	if [ -z "$missing" ]; then
		[ "$dry_run" = 0 ] || say "    python3 and git are present"
		return
	fi
	hint=''
	if [ "$os" = Darwin ]; then
		hint='brew install python git'
	elif have apt-get; then
		hint='sudo apt-get install python3 git'
	elif have dnf; then
		hint='sudo dnf install python3 git'
	elif have yum; then
		hint='sudo yum install python3 git'
	elif have pacman; then
		hint='sudo pacman -S python git'
	elif have zypper; then
		hint='sudo zypper install python3 git'
	elif have apk; then
		hint='sudo apk add python3 git'
	fi
	note "the skill's scripts need $missing.${hint:+ Install with: $hint}"
}

dry_run_report() {
	say "Dry run: nothing is downloaded or changed."
	say "==> Would download for $platform from $base"
	if [ "$bin_only" = 1 ]; then
		say "    SHA256SUMS, $bin_tar"
	else
		say "    SHA256SUMS, $bin_tar, envrelay-skill.tar.gz"
	fi
	say "==> envrelay"
	say "    would install $bin_dir/envrelay$(version_note)"
	if [ "$bin_only" = 0 ]; then
		say "==> Skill"
		plan_skill
	fi
	say "==> PATH"
	setup_path
	say "==> python3 and git"
	check_tools
	print_notes
}

uninstall() {
	[ "$dry_run" = 0 ] || say "Dry run: nothing is removed."
	say "==> Removing EnvRelay"
	if [ -f "$bin_dir/envrelay" ] || [ -L "$bin_dir/envrelay" ]; then
		if [ "$dry_run" = 1 ]; then
			say "    would remove $bin_dir/envrelay"
		else
			rm -f "$bin_dir/envrelay"
			say "    removed $bin_dir/envrelay"
		fi
	else
		say "    no envrelay in $bin_dir"
	fi
	case $(skill_state) in
	ours)
		each_link_dir unlink_one
		if [ "$dry_run" = 1 ]; then
			say "    would remove $canonical"
		else
			rm -rf "$canonical"
			say "    removed $canonical"
		fi
		;;
	theirs) note "left $canonical as it is: this installer did not put it there." ;;
	absent) each_link_dir unlink_one ;;
	esac
	for f in "${ZDOTDIR:-$HOME}/.zshrc" "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.bash_login" \
		"$HOME/.profile" "${XDG_CONFIG_HOME:-$HOME/.config}/fish/conf.d/envrelay.fish"; do
		if [ -f "$f" ] && grep -Fqx "$PATH_COMMENT" "$f"; then
			note "kept the PATH line in $f, since other programs may use that directory. Delete it and the comment above it if you like."
		fi
	done
	note "backups (.envrelay files) are yours: the installer never touches them."
	print_notes
}

main() {
	version='' bin_dir=${ENVRELAY_BIN_DIR:-} bin_only=0 modify_path=1 dry_run=0 remove=0
	notes='' tmp='' staged_bin='' staged_skill='' old_skill='' installed_version=''
	while [ $# -gt 0 ]; do
		case $1 in
		--version)
			[ $# -ge 2 ] || die "--version needs a value"
			version=$2
			shift
			;;
		--version=*) version=${1#*=} ;;
		--bin-dir)
			[ $# -ge 2 ] || die "--bin-dir needs a value"
			bin_dir=$2
			shift
			;;
		--bin-dir=*) bin_dir=${1#*=} ;;
		--bin-only) bin_only=1 ;;
		--no-modify-path) modify_path=0 ;;
		--dry-run) dry_run=1 ;;
		--uninstall) remove=1 ;;
		-h | --help)
			usage
			return
			;;
		*) die "unknown option: $1 (see --help)" ;;
		esac
		shift
	done

	if [ -z "${HOME:-}" ] || [ ! -d "$HOME" ]; then die "HOME is not set to a directory"; fi
	if [ "$(id -u)" = 0 ] && [ -n "${SUDO_USER:-}" ]; then
		die "run this without sudo: it installs into your own home directory"
	fi
	resolve_paths
	if [ "$remove" = 1 ]; then
		uninstall
		return
	fi

	detect_platform
	[ -n "$version" ] || version=$(skill_version)
	version=${version#v}
	case $version in
	*[!0-9A-Za-z.+-]*) die "not a version: $version" ;;
	esac
	if [ -n "$version" ]; then
		base=https://github.com/$REPO/releases/download/v$version
	else
		base=https://github.com/$REPO/releases/latest/download
	fi
	bin_tar=envrelay-$asset.tar.gz

	if [ "$dry_run" = 1 ]; then
		dry_run_report
		return
	fi

	trap cleanup EXIT
	trap 'exit 129' HUP
	trap 'exit 130' INT
	trap 'exit 143' TERM
	tmp=$(mktemp -d 2>/dev/null || mktemp -d -t envrelay) || die "could not create a temporary directory"

	# Everything is downloaded and checked before anything is changed.
	say "==> Downloading EnvRelay for $platform"
	fetch "$base/SHA256SUMS" "$tmp/SHA256SUMS"
	fetch "$base/$bin_tar" "$tmp/$bin_tar"
	verify "$tmp/$bin_tar" "$bin_tar"
	mkdir "$tmp/bin"
	tar -xzof "$tmp/$bin_tar" -C "$tmp/bin" || die "could not unpack $bin_tar"
	if [ "$bin_only" = 0 ] && [ "$(skill_state)" != theirs ]; then
		fetch "$base/envrelay-skill.tar.gz" "$tmp/envrelay-skill.tar.gz"
		verify "$tmp/envrelay-skill.tar.gz" envrelay-skill.tar.gz
		mkdir "$tmp/skill"
		tar -xzof "$tmp/envrelay-skill.tar.gz" -C "$tmp/skill" || die "could not unpack envrelay-skill.tar.gz"
	fi

	say "==> Installing"
	install_binary
	[ "$bin_only" = 1 ] || install_skill
	setup_path
	check_shadowing
	check_tools

	say ""
	if [ "$bin_only" = 1 ]; then
		say "$installed_version is installed: $bin_dir/envrelay"
		print_notes
		return
	fi
	say "EnvRelay is installed: $installed_version and the skill."
	print_notes
	say ""
	say "Next: start a new session of your coding agent and ask it to back up this"
	say "machine's development environment. It proposes what to carry, copies what"
	say "you approve, and gives you one envrelay command to run yourself: you type"
	say "the passphrase in your own terminal, and it never passes through the agent."
}

main "$@"
