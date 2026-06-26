//! Denial message box renderer for terminal output.
//!
//! Provides a rich denial message display with:
//! - Bordered box with header
//! - Command with span highlighting
//! - Pattern name and severity
//! - Optional explanation text
//! - Safe alternatives as bullet list
//!
//! Falls back to plain text format for non-TTY contexts.

use super::theme::{BorderStyle, Severity, Theme};
use crate::highlight::{HighlightSpan, format_highlighted_command};
#[cfg(feature = "rich-output")]
use crate::output::rich_theme::{RichThemeExt, color_to_markup};
use crate::output::terminal_width;
#[cfg(not(feature = "rich-output"))]
use ratatui::style::Color;
#[cfg(feature = "rich-output")]
#[allow(unused_imports)]
use rich_rust::prelude::*;
use std::fmt::Write;

/// A denial message box to display when a command is blocked.
#[derive(Debug, Clone)]
pub struct DenialBox {
    /// The blocked command.
    pub command: String,
    /// Span within the command that matched.
    pub span: HighlightSpan,
    /// Pattern identifier (e.g., "`core.git:reset-hard`" or "`core.git.reset_hard`").
    pub pattern_id: String,
    /// Severity level of the match.
    pub severity: Severity,
    /// Optional explanation of why this command is blocked.
    pub explanation: Option<String>,
    /// Suggested safe alternatives.
    pub alternatives: Vec<String>,
    /// Optional allow-once code.
    pub allow_once_code: Option<String>,
}

impl DenialBox {
    /// Create a new denial box.
    #[must_use]
    pub fn new(
        command: impl Into<String>,
        span: HighlightSpan,
        pattern_id: impl Into<String>,
        severity: Severity,
    ) -> Self {
        Self {
            command: command.into(),
            span,
            pattern_id: pattern_id.into(),
            severity,
            explanation: None,
            alternatives: Vec::new(),
            allow_once_code: None,
        }
    }

    /// Add an explanation.
    #[must_use]
    pub fn with_explanation(mut self, explanation: impl Into<String>) -> Self {
        let explanation = explanation.into();
        let trimmed = explanation.trim();
        if trimmed.is_empty() {
            self.explanation = None;
        } else if trimmed.len() == explanation.len() {
            self.explanation = Some(explanation);
        } else {
            self.explanation = Some(trimmed.to_string());
        }
        self
    }

    /// Add safe alternatives.
    #[must_use]
    pub fn with_alternatives(mut self, alternatives: Vec<String>) -> Self {
        self.alternatives = alternatives;
        self
    }

    /// Add allow-once code.
    #[must_use]
    pub fn with_allow_once_code(mut self, code: impl Into<String>) -> Self {
        self.allow_once_code = Some(code.into());
        self
    }

    /// Render the denial box with the given theme.
    ///
    /// Uses rich_rust when the feature is enabled, otherwise falls back to
    /// manual rendering.
    #[must_use]
    pub fn render(&self, theme: &Theme) -> String {
        #[cfg(feature = "rich-output")]
        {
            // If using rich output, delegate to render_rich
            self.render_rich(theme)
        }
        #[cfg(not(feature = "rich-output"))]
        match theme.border_style {
            BorderStyle::Unicode => {
                let output = self.render_unicode(theme);
                if theme.colors_enabled {
                    output
                } else {
                    strip_ansi_codes(&output)
                }
            }
            BorderStyle::Ascii => self.render_ascii(theme),
            BorderStyle::None => {
                let output = self.render_minimal(theme);
                if theme.colors_enabled {
                    output
                } else {
                    strip_ansi_codes(&output)
                }
            }
        }
    }

    /// Render with rich_rust (Premium UI).
    #[cfg(feature = "rich-output")]
    fn render_rich(&self, theme: &Theme) -> String {
        use rich_rust::r#box::{ASCII, DOUBLE, HEAVY, MINIMAL, ROUNDED};
        use rich_rust::prelude::*;

        let pattern_lines =
            format_pattern_lines(&self.pattern_id, theme.severity_label(self.severity));
        let width = terminal_width().saturating_sub(8).max(40) as usize;

        // Build content as a Vec of lines
        let mut lines = Vec::new();

        // 1. Header is handled by Panel title, but we add inner padding text
        let severity_markup = theme.severity_markup(self.severity);
        lines.push(format!("[{severity_markup}]🛑 COMMAND BLOCKED[/]"));
        lines.push(String::new());

        // 2. Command with highlighting
        // Note: We use manual highlighting for now, but rich_rust Syntax could be used later
        lines.push(format!("[dim]Command:[/]  [bold]{}[/]", self.command));

        // 3. Explanation
        if let Some(explanation) = &self.explanation {
            lines.push(String::new());
            lines.push(format!("[{severity_markup}]Explanation:[/]"));
            for line in wrap_text(explanation, width) {
                lines.push(line);
            }
        }

        // 4. Pattern Info
        lines.push(String::new());
        for line in pattern_lines {
            lines.push(format!("[dim]{line}[/]"));
        }

        // 5. Alternatives
        if !self.alternatives.is_empty() {
            lines.push(String::new());
            lines.push(format!("[{}]Safe alternatives:[/]", theme.success_markup()));
            for alt in &self.alternatives {
                lines.push(format!("  [green]•[/] {alt}"));
            }
        }

        // 6. Allow-once code
        if let Some(code) = &self.allow_once_code {
            lines.push(String::new());
            lines.push("[dim]─────────────────────────────────────[/]".to_string());
            lines.push(format!(
                "[yellow]To allow once:[/] [bold]dcg allow-once {code}[/]"
            ));
        }

        let content_str = lines.join("\n");

        // Determine border style and color
        let box_style: &'static rich_rust::r#box::BoxChars = match theme.border_style {
            BorderStyle::Unicode => match self.severity {
                Severity::Critical => &DOUBLE,
                Severity::High => &HEAVY,
                _ => &ROUNDED,
            },
            BorderStyle::Ascii => &ASCII,
            BorderStyle::None => &MINIMAL,
        };

        let border_color = color_to_markup(theme.color_for_severity(self.severity));

        // Create Panel
        Panel::from_text(&content_str)
            .title("[bold] DCG [/]")
            .border_style(Style::parse(&border_color).unwrap_or_default())
            .box_style(box_style)
            .padding((1, 2))
            .render_plain(width)
    }

    /// Render a plain text version for non-TTY contexts.
    #[must_use]
    pub fn render_plain(&self) -> String {
        let mut output = String::new();
        let width = terminal_width().saturating_sub(4).max(40) as usize;
        let severity_label = format!("{:?}", self.severity).to_uppercase();
        let pattern_lines = format_pattern_lines(&self.pattern_id, &severity_label);

        // Header
        let _ = writeln!(output, "BLOCKED: Destructive Command Detected");
        let _ = writeln!(output);

        // Command with highlighting
        let highlighted =
            format_highlighted_command(&self.command, &self.span, false, terminal_width().into());
        let _ = writeln!(output, "  Command: {}", highlighted.command_line);
        let _ = writeln!(output, "           {}", highlighted.caret_line);
        if let Some(label) = &highlighted.label_line {
            let _ = writeln!(output, "           {label}");
        }
        let _ = writeln!(output);

        // Explanation
        if let Some(explanation) = &self.explanation {
            let _ = writeln!(output);
            let _ = writeln!(output, "  Explanation:");
            for line in wrap_text(explanation, width.saturating_sub(2)) {
                let _ = writeln!(output, "  {line}");
            }
        }

        // Pattern info
        let _ = writeln!(output);
        for line in pattern_lines {
            let _ = writeln!(output, "  {line}");
        }

        // Alternatives
        if !self.alternatives.is_empty() {
            let _ = writeln!(output);
            let _ = writeln!(output, "  Safe alternatives:");
            for alt in &self.alternatives {
                let _ = writeln!(output, "    - {alt}");
            }
        }

        output
    }

    /// Render with Unicode box-drawing characters.
    #[cfg(not(feature = "rich-output"))]
    #[allow(clippy::too_many_lines)]
    fn render_unicode(&self, theme: &Theme) -> String {
        let width = terminal_width().saturating_sub(4).max(40) as usize;
        let mut output = String::new();
        let severity_code = severity_color_code(theme, self.severity);
        let success_code = ansi_color_code(theme.success_color);
        let pattern_lines =
            format_pattern_lines(&self.pattern_id, theme.severity_label(self.severity));
        let explanation_label = format!("\x1b[1;{}mExplanation:\x1b[0m", &severity_code);

        // Top border with header
        let header = " \u{26d4}  BLOCKED: Destructive Command Detected ";
        let header_len = header.chars().count();
        let top_pad = width.saturating_sub(header_len);

        let _ = writeln!(
            output,
            "\x1b[{}m\u{256d}{}\u{256e}\x1b[0m",
            &severity_code,
            "\u{2500}".repeat(width)
        );
        let _ = writeln!(
            output,
            "\x1b[{}m\u{2502}\x1b[0m\x1b[1;{}m{}\x1b[0m{}\x1b[{}m\u{2502}\x1b[0m",
            &severity_code,
            &severity_code,
            header,
            " ".repeat(top_pad),
            &severity_code
        );
        let _ = writeln!(
            output,
            "\x1b[{}m\u{251c}{}\u{2524}\x1b[0m",
            &severity_code,
            "\u{2500}".repeat(width)
        );

        // Command section
        let highlighted = format_highlighted_command(
            &self.command,
            &self.span,
            theme.colors_enabled,
            width.saturating_sub(4),
        );

        let _ = writeln!(
            output,
            "\x1b[{}m\u{2502}\x1b[0m  {}{}  \x1b[{}m\u{2502}\x1b[0m",
            &severity_code,
            highlighted.command_line,
            padding_for(&highlighted.command_line, width.saturating_sub(4)),
            &severity_code
        );
        let _ = writeln!(
            output,
            "\x1b[{}m\u{2502}\x1b[0m  {}{}  \x1b[{}m\u{2502}\x1b[0m",
            &severity_code,
            highlighted.caret_line,
            padding_for(&highlighted.caret_line, width.saturating_sub(4)),
            &severity_code
        );
        if let Some(label) = &highlighted.label_line {
            let _ = writeln!(
                output,
                "\x1b[{}m\u{2502}\x1b[0m  {}{}  \x1b[{}m\u{2502}\x1b[0m",
                &severity_code,
                label,
                padding_for(label, width.saturating_sub(4)),
                &severity_code
            );
        }

        // Empty line
        let _ = writeln!(
            output,
            "\x1b[{}m\u{2502}\x1b[0m{}  \x1b[{}m\u{2502}\x1b[0m",
            &severity_code,
            " ".repeat(width.saturating_sub(2)),
            &severity_code
        );

        // Explanation
        if let Some(explanation) = &self.explanation {
            let _ = writeln!(
                output,
                "\x1b[{}m\u{2502}\x1b[0m{}  \x1b[{}m\u{2502}\x1b[0m",
                &severity_code,
                " ".repeat(width.saturating_sub(2)),
                &severity_code
            );

            let _ = writeln!(
                output,
                "\x1b[{}m\u{2502}\x1b[0m  {}{}  \x1b[{}m\u{2502}\x1b[0m",
                &severity_code,
                explanation_label,
                padding_for(&explanation_label, width.saturating_sub(4)),
                &severity_code
            );

            // Word wrap explanation
            for line in wrap_text(explanation, width.saturating_sub(4)) {
                let _ = writeln!(
                    output,
                    "\x1b[{}m\u{2502}\x1b[0m  {}{}  \x1b[{}m\u{2502}\x1b[0m",
                    &severity_code,
                    line,
                    padding_for(&line, width.saturating_sub(4)),
                    &severity_code
                );
            }
        }

        // Pattern info
        let _ = writeln!(
            output,
            "\x1b[{}m\u{2502}\x1b[0m{}  \x1b[{}m\u{2502}\x1b[0m",
            &severity_code,
            " ".repeat(width.saturating_sub(2)),
            &severity_code
        );
        for pattern_line in pattern_lines {
            let _ = writeln!(
                output,
                "\x1b[{}m\u{2502}\x1b[0m  \x1b[2m{}\x1b[0m{}  \x1b[{}m\u{2502}\x1b[0m",
                &severity_code,
                pattern_line,
                padding_for(&pattern_line, width.saturating_sub(4)),
                &severity_code
            );
        }

        // Alternatives
        if !self.alternatives.is_empty() {
            let _ = writeln!(
                output,
                "\x1b[{}m\u{2502}\x1b[0m{}  \x1b[{}m\u{2502}\x1b[0m",
                &severity_code,
                " ".repeat(width.saturating_sub(2)),
                &severity_code
            );

            let alt_header = "Safe alternatives:";
            let _ = writeln!(
                output,
                "\x1b[{}m\u{2502}\x1b[0m  \x1b[{}m{}\x1b[0m{}  \x1b[{}m\u{2502}\x1b[0m",
                &severity_code,
                &success_code,
                alt_header,
                padding_for(alt_header, width.saturating_sub(4)),
                &severity_code
            );

            for alt in &self.alternatives {
                let bullet_line = format!("\u{2022} {alt}");
                let _ = writeln!(
                    output,
                    "\x1b[{}m\u{2502}\x1b[0m    \x1b[{}m{}\x1b[0m{}  \x1b[{}m\u{2502}\x1b[0m",
                    &severity_code,
                    &success_code,
                    bullet_line,
                    padding_for(&bullet_line, width.saturating_sub(6)),
                    &severity_code
                );
            }
        }

        // Bottom border
        let _ = writeln!(
            output,
            "\x1b[{}m\u{2570}{}\u{256f}\x1b[0m",
            &severity_code,
            "\u{2500}".repeat(width)
        );

        output
    }

    /// Render with ASCII box-drawing characters.
    #[cfg(not(feature = "rich-output"))]
    fn render_ascii(&self, theme: &Theme) -> String {
        let width = terminal_width().saturating_sub(4).max(40) as usize;
        let mut output = String::new();
        let pattern_lines =
            format_pattern_lines(&self.pattern_id, theme.severity_label(self.severity));

        // Top border with header
        let header = " !  BLOCKED: Destructive Command Detected ";
        let header_len = header.chars().count();
        let top_pad = width.saturating_sub(header_len);

        let _ = writeln!(output, "+{}+", "-".repeat(width));
        let _ = writeln!(output, "|{}{}|", header, " ".repeat(top_pad));
        let _ = writeln!(output, "+{}+", "-".repeat(width));

        // Command section
        let highlighted = format_highlighted_command(
            &self.command,
            &self.span,
            theme.colors_enabled,
            width.saturating_sub(4),
        );

        let _ = writeln!(
            output,
            "|  {}{}  |",
            highlighted.command_line,
            padding_for(&highlighted.command_line, width.saturating_sub(4))
        );
        let _ = writeln!(
            output,
            "|  {}{}  |",
            highlighted.caret_line,
            padding_for(&highlighted.caret_line, width.saturating_sub(4))
        );
        if let Some(label) = &highlighted.label_line {
            let _ = writeln!(
                output,
                "|  {}{}  |",
                label,
                padding_for(label, width.saturating_sub(4))
            );
        }

        // Empty line
        let _ = writeln!(output, "|{}  |", " ".repeat(width.saturating_sub(2)));

        // Explanation
        if let Some(explanation) = &self.explanation {
            let _ = writeln!(output, "|{}  |", " ".repeat(width.saturating_sub(2)));
            let explanation_label = "EXPLANATION:";
            let _ = writeln!(
                output,
                "|  {}{}  |",
                explanation_label,
                padding_for(explanation_label, width.saturating_sub(4))
            );
            for line in wrap_text(explanation, width.saturating_sub(4)) {
                let _ = writeln!(
                    output,
                    "|  {}{}  |",
                    line,
                    padding_for(&line, width.saturating_sub(4))
                );
            }
        }

        // Pattern info
        let _ = writeln!(output, "|{}  |", " ".repeat(width.saturating_sub(2)));
        for pattern_line in pattern_lines {
            let _ = writeln!(
                output,
                "|  {}{}  |",
                pattern_line,
                padding_for(&pattern_line, width.saturating_sub(4))
            );
        }

        // Alternatives
        if !self.alternatives.is_empty() {
            let _ = writeln!(output, "|{}  |", " ".repeat(width.saturating_sub(2)));
            let alt_header = "Safe alternatives:";
            let _ = writeln!(
                output,
                "|  {}{}  |",
                alt_header,
                padding_for(alt_header, width.saturating_sub(4))
            );
            for alt in &self.alternatives {
                let bullet_line = format!("* {alt}");
                let _ = writeln!(
                    output,
                    "|    {}{}  |",
                    bullet_line,
                    padding_for(&bullet_line, width.saturating_sub(6))
                );
            }
        }

        // Bottom border
        let _ = writeln!(output, "+{}+", "-".repeat(width));

        output
    }

    /// Render with no borders (minimal style).
    #[cfg(not(feature = "rich-output"))]
    fn render_minimal(&self, theme: &Theme) -> String {
        let mut output = String::new();
        let severity_code = severity_color_code(theme, self.severity);
        let success_code = ansi_color_code(theme.success_color);
        let pattern_lines =
            format_pattern_lines(&self.pattern_id, theme.severity_label(self.severity));

        // Header with color
        let _ = writeln!(
            output,
            "\x1b[{}m\u{26d4}  BLOCKED\x1b[0m: Destructive Command Detected",
            &severity_code
        );
        let _ = writeln!(output);

        // Command with highlighting
        let width = terminal_width().saturating_sub(4).max(40);
        let highlighted = format_highlighted_command(
            &self.command,
            &self.span,
            theme.colors_enabled,
            width.into(),
        );

        let _ = writeln!(output, "  {}", highlighted.command_line);
        let _ = writeln!(output, "  {}", highlighted.caret_line);
        if let Some(label) = &highlighted.label_line {
            let _ = writeln!(output, "  {label}");
        }
        let _ = writeln!(output);

        // Explanation
        if let Some(explanation) = &self.explanation {
            let _ = writeln!(output);
            let explanation_label = format!("\x1b[1;{}mExplanation:\x1b[0m", &severity_code);
            let width = terminal_width().saturating_sub(4).max(40) as usize;
            let _ = writeln!(output, "  {explanation_label}");
            for line in wrap_text(explanation, width.saturating_sub(2)) {
                let _ = writeln!(output, "  {line}");
            }
        }

        // Pattern info
        let _ = writeln!(output);
        for pattern_line in pattern_lines {
            let _ = writeln!(output, "  \x1b[2m{pattern_line}\x1b[0m");
        }

        // Alternatives
        if !self.alternatives.is_empty() {
            let _ = writeln!(output);
            let _ = writeln!(output, "  \x1b[{}mSafe alternatives:\x1b[0m", &success_code);
            for alt in &self.alternatives {
                let _ = writeln!(output, "    \x1b[{}m\u{2022}\x1b[0m {alt}", &success_code);
            }
        }

        output
    }
}

/// Convert a ratatui color to an ANSI foreground color code sequence.
#[cfg(not(feature = "rich-output"))]
fn ansi_color_code(color: Color) -> String {
    match color {
        Color::Reset => "0".to_string(),
        Color::Black => "30".to_string(),
        Color::Red => "31".to_string(),
        Color::Green => "32".to_string(),
        Color::Yellow => "33".to_string(),
        Color::Blue => "34".to_string(),
        Color::Magenta => "35".to_string(),
        Color::Cyan => "36".to_string(),
        Color::Gray => "37".to_string(),
        Color::DarkGray => "90".to_string(),
        Color::LightRed => "91".to_string(),
        Color::LightGreen => "92".to_string(),
        Color::LightYellow => "93".to_string(),
        Color::LightBlue => "94".to_string(),
        Color::LightMagenta => "95".to_string(),
        Color::LightCyan => "96".to_string(),
        Color::White => "97".to_string(),
        Color::Rgb(r, g, b) => format!("38;2;{r};{g};{b}"),
        Color::Indexed(index) => format!("38;5;{index}"),
    }
}

/// Get ANSI color code for severity level.
#[cfg(not(feature = "rich-output"))]
fn severity_color_code(theme: &Theme, severity: Severity) -> String {
    ansi_color_code(theme.color_for_severity(severity))
}

/// Calculate padding needed to fill width, accounting for ANSI codes.
#[cfg(not(feature = "rich-output"))]
fn padding_for(text: &str, width: usize) -> String {
    let visible_len = strip_ansi_codes(text).chars().count();
    let padding = width.saturating_sub(visible_len);
    " ".repeat(padding)
}

/// Strip ANSI escape codes from a string to get visible length.
#[cfg(not(feature = "rich-output"))]
fn strip_ansi_codes(s: &str) -> String {
    let mut result = String::with_capacity(s.len());
    let mut in_escape = false;

    for c in s.chars() {
        if c == '\x1b' {
            in_escape = true;
            continue;
        }
        if in_escape {
            if c == 'm' {
                in_escape = false;
            }
            continue;
        }
        result.push(c);
    }

    result
}

/// Wrap text to fit within the specified width (character count, not bytes).
fn wrap_text(text: &str, width: usize) -> Vec<String> {
    if text.is_empty() || width == 0 {
        return vec![];
    }

    let mut lines = Vec::new();

    for raw_line in text.lines() {
        if raw_line.is_empty() {
            lines.push(String::new());
            continue;
        }

        let prefix_len = raw_line.chars().take_while(|c| c.is_whitespace()).count();
        let prefix: String = raw_line.chars().take(prefix_len).collect();
        let content = raw_line[prefix_len..].trim_end();

        if content.is_empty() {
            lines.push(String::new());
            continue;
        }

        let mut current_line = String::new();
        let mut current_char_count = 0;

        for word in content.split_whitespace() {
            let word_char_count = word.chars().count();
            if current_line.is_empty() {
                current_line = format!("{prefix}{word}");
                current_char_count = prefix_len + word_char_count;
            } else if current_char_count + 1 + word_char_count <= width {
                current_line.push(' ');
                current_line.push_str(word);
                current_char_count += 1 + word_char_count;
            } else {
                lines.push(current_line);
                current_line = format!("{prefix}{word}");
                current_char_count = prefix_len + word_char_count;
            }
        }

        if !current_line.is_empty() {
            lines.push(current_line);
        }
    }

    lines
}

/// Split a pattern identifier into (pack, pattern) if possible.
fn split_pattern_id(pattern_id: &str) -> (Option<&str>, &str) {
    if let Some((pack, pattern)) = pattern_id.split_once(':') {
        if !pack.is_empty() && !pattern.is_empty() {
            return (Some(pack), pattern);
        }
    }

    let dot_count = pattern_id.chars().filter(|c| *c == '.').count();
    if dot_count >= 2 {
        if let Some(idx) = pattern_id.rfind('.') {
            let (pack, pattern) = pattern_id.split_at(idx);
            let pattern = &pattern[1..];
            if !pack.is_empty() && !pattern.is_empty() {
                return (Some(pack), pattern);
            }
        }
    }

    (None, pattern_id)
}

fn format_pattern_lines(pattern_id: &str, severity_label: &str) -> Vec<String> {
    let (pack, pattern) = split_pattern_id(pattern_id);
    match pack {
        Some(pack_id) => vec![
            format!("Pattern: {pattern}"),
            format!("Pack: {pack_id} (severity: {severity_label})"),
        ],
        None => vec![format!("Pattern: {pattern} ({severity_label})")],
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_denial_box_plain_render() {
        let span = HighlightSpan::with_label(0, 16, "Matched: git reset --hard");
        let denial = DenialBox::new(
            "git reset --hard HEAD",
            span,
            "core.git.reset_hard",
            Severity::Critical,
        );

        let output = denial.render_plain();

        assert!(output.contains("BLOCKED"));
        assert!(output.contains("git reset --hard"));
        assert!(output.contains("Pattern: reset_hard"));
        assert!(output.contains("Pack: core.git"));
        assert!(output.contains("CRITICAL"));
    }

    #[test]
    fn test_denial_box_with_explanation() {
        let span = HighlightSpan::new(0, 10);
        let denial = DenialBox::new(
            "rm -rf /",
            span,
            "core.filesystem.rm_rf",
            Severity::Critical,
        )
        .with_explanation("This command would delete all files on the system.");

        let output = denial.render_plain();

        assert!(output.contains("would delete all files"));
    }

    #[test]
    fn test_denial_box_with_alternatives() {
        let span = HighlightSpan::new(0, 10);
        let denial = DenialBox::new(
            "rm -rf /tmp/foo",
            span,
            "core.filesystem.rm_rf",
            Severity::Medium,
        )
        .with_alternatives(vec![
            "rm -ri /tmp/foo (interactive)".to_string(),
            "mv /tmp/foo /tmp/foo.bak (backup first)".to_string(),
        ]);

        let output = denial.render_plain();

        assert!(output.contains("Safe alternatives:"));
        assert!(output.contains("interactive"));
        assert!(output.contains("backup first"));
    }

    #[test]
    #[cfg(not(feature = "rich-output"))]
    fn test_denial_box_unicode_render() {
        let span = HighlightSpan::new(0, 10);
        let theme = Theme::default();
        let denial = DenialBox::new(
            "git push --force",
            span,
            "core.git.force_push",
            Severity::High,
        );

        let output = denial.render(&theme);

        // Should contain Unicode box-drawing characters
        assert!(output.contains('\u{256d}')); // Top-left corner
        assert!(output.contains('\u{256f}')); // Bottom-right corner
        assert!(output.contains("BLOCKED"));
    }

    #[test]
    #[cfg(not(feature = "rich-output"))]
    fn test_denial_box_ascii_render() {
        let span = HighlightSpan::new(0, 10);
        let theme = Theme {
            border_style: BorderStyle::Ascii,
            colors_enabled: true,
            ..Default::default()
        };
        let denial = DenialBox::new(
            "git push --force",
            span,
            "core.git.force_push",
            Severity::High,
        );

        let output = denial.render(&theme);

        // Should use ASCII characters
        assert!(output.contains('+'));
        assert!(output.contains('-'));
        assert!(output.contains("BLOCKED"));
    }

    #[test]
    #[cfg(not(feature = "rich-output"))]
    fn test_denial_box_no_color_still_uses_ascii_box() {
        let span = HighlightSpan::new(0, 10);
        let theme = Theme::no_color();
        let denial = DenialBox::new(
            "git push --force",
            span,
            "core.git.force_push",
            Severity::High,
        );

        let output = denial.render(&theme);

        assert!(output.contains('+'));
        assert!(output.contains("BLOCKED"));
        assert!(
            !output.contains('\x1b'),
            "No ANSI escapes should appear when colors are disabled"
        );
    }

    #[test]
    #[cfg(not(feature = "rich-output"))]
    fn test_denial_box_unicode_without_colors_strips_ansi() {
        let span = HighlightSpan::new(0, 10);
        let theme = Theme::default().without_colors();
        let denial = DenialBox::new(
            "git push --force",
            span,
            "core.git.force_push",
            Severity::High,
        );

        let output = denial.render(&theme);

        assert!(output.contains('\u{256d}'));
        assert!(output.contains("BLOCKED"));
        assert!(
            !output.contains('\x1b'),
            "No ANSI escapes should appear when colors are disabled"
        );
    }

    #[test]
    fn test_wrap_text() {
        let text =
            "This is a long explanation that needs to be wrapped to fit within the terminal width.";
        let wrapped = wrap_text(text, 30);

        assert!(wrapped.len() > 1);
        for line in &wrapped {
            assert!(line.len() <= 30);
        }
    }

    #[test]
    #[cfg(not(feature = "rich-output"))]
    fn test_strip_ansi_codes() {
        let with_codes = "\x1b[31mRed text\x1b[0m and \x1b[32mgreen\x1b[0m";
        let stripped = strip_ansi_codes(with_codes);

        assert_eq!(stripped, "Red text and green");
    }

    #[test]
    #[cfg(not(feature = "rich-output"))]
    fn test_severity_color_codes() {
        let theme = Theme::default();
        assert_eq!(severity_color_code(&theme, Severity::Critical), "31");
        assert_eq!(severity_color_code(&theme, Severity::High), "91");
        assert_eq!(severity_color_code(&theme, Severity::Medium), "33");
        assert_eq!(severity_color_code(&theme, Severity::Low), "34");
    }

    #[test]
    fn test_denial_box_unicode_command_preservation() {
        // Verify Unicode characters in commands are preserved
        let cmd = "rm -rf /path/with/émojis/🎉/and/中文";
        let span = HighlightSpan::new(0, 5);
        let denial = DenialBox::new(cmd, span, "core.filesystem.rm_rf", Severity::Critical);

        let output = denial.render_plain();

        assert!(
            output.contains("émojis"),
            "Unicode accented characters must be preserved"
        );
        assert!(output.contains("🎉"), "Emoji must be preserved");
        assert!(output.contains("中文"), "CJK characters must be preserved");
    }

    #[test]
    fn test_denial_box_all_severity_levels() {
        // Verify all severity levels render correctly
        for severity in [
            Severity::Critical,
            Severity::High,
            Severity::Medium,
            Severity::Low,
        ] {
            let span = HighlightSpan::new(0, 10);
            let denial = DenialBox::new("test command", span, "test.pattern", severity);
            let output = denial.render_plain();

            assert!(
                output.contains("BLOCKED"),
                "All severities must show BLOCKED header"
            );
            assert!(
                output.contains(&format!("{severity:?}").to_uppercase()),
                "Output must contain severity level: {severity:?}"
            );
        }
    }

    #[test]
    #[cfg(not(feature = "rich-output"))]
    fn test_denial_box_minimal_render() {
        let span = HighlightSpan::new(0, 10);
        let theme = Theme {
            border_style: BorderStyle::None,
            ..Default::default()
        };
        let denial = DenialBox::new(
            "git push --force",
            span,
            "core.git.force_push",
            Severity::High,
        );

        let output = denial.render(&theme);
        let clean_output = strip_ansi_codes(&output);

        // Minimal style should still contain key elements
        assert!(clean_output.contains("BLOCKED"));
        // Highlighting might split the command with ANSI codes, but clean_output handles that
        assert!(clean_output.contains("git push --force"));
        assert!(clean_output.contains("Pattern: force_push"));
        assert!(clean_output.contains("Pack: core.git"));
    }

    #[test]
    fn test_wrap_text_empty_input() {
        let wrapped = wrap_text("", 30);
        assert!(wrapped.is_empty());
    }

    #[test]
    fn test_wrap_text_zero_width() {
        let wrapped = wrap_text("some text", 0);
        assert!(wrapped.is_empty());
    }

    #[test]
    fn test_wrap_text_single_word() {
        let wrapped = wrap_text("word", 30);
        assert_eq!(wrapped.len(), 1);
        assert_eq!(wrapped[0], "word");
    }

    #[test]
    #[cfg(not(feature = "rich-output"))]
    fn test_padding_for_with_ansi() {
        // Text with ANSI codes should be padded based on visible length
        let text_with_ansi = "\x1b[31mRed\x1b[0m";
        let padding = padding_for(text_with_ansi, 10);
        // Visible length is 3 ("Red"), so padding should be 7 spaces
        assert_eq!(padding.len(), 7);
    }
}
