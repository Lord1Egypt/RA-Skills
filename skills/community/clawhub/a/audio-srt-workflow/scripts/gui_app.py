#!/usr/bin/env python3
"""Desktop GUI MVP for subtitle generation and text-audio alignment."""

from __future__ import annotations

import threading
import traceback
from argparse import Namespace
from datetime import datetime
from pathlib import Path
import multiprocessing as mp
from typing import Callable, Optional

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Tkinter is not available in this Python environment. "
        "Please install/enable Tk support."
    ) from exc

from align_to_srt import (
    AlignmentConfig,
    AutoSubtitleRunResult,
    build_alignment_config,
    resolve_output_path,
    run_alignment_pipeline,
    run_auto_subtitle_pipeline,
)

UI_TEXTS = {
    "en": {
        "window_title": "Audio SRT Tool - GUI MVP",
        "ui_lang_label": "UI Language",
        "common_config": "Common Config",
        "run_log": "Run Log",
        "tab_auto": "Auto Subtitle (Audio)",
        "tab_align": "Align With Text",
        "browse": "Browse",
        "run_auto": "Run Auto Subtitle",
        "run_align": "Run Text Alignment",
        "label_model": "Model",
        "label_asr_language": "ASR Language",
        "label_device": "Device",
        "label_compute_type": "Compute Type",
        "label_beam_size": "Beam Size",
        "label_start_lag": "Start Lag (s)",
        "label_end_hold": "End Hold (s)",
        "label_min_gap": "Min Gap (s)",
        "label_snap_window": "Snap Window (s)",
        "label_max_unit_duration": "Max Unit Duration",
        "label_split_pause_gap": "Split Pause Gap",
        "label_max_split_depth": "Max Split Depth",
        "label_max_early_lead": "Max Early Lead",
        "label_anchor_min_voice": "Anchor Min Voice",
        "label_onset_lookahead": "Onset Lookahead",
        "label_tail_end_guard": "Tail End Guard",
        "label_audio": "Audio",
        "label_transcript_text": "Transcript Text",
        "label_output_srt": "Output SRT",
        "check_disable_waveform_snap": "Disable waveform snap",
        "check_date_suffix": "Add date suffix to output",
        "dialog_select_audio": "Select audio file",
        "dialog_select_text": "Select text file",
        "dialog_select_output_srt": "Select output SRT file",
        "filetype_audio": "Audio Files",
        "filetype_text": "Text Files",
        "filetype_srt": "SRT Files",
        "filetype_all": "All Files",
        "warn_running_title": "Running",
        "warn_running_body": "A task is still running. Please wait.",
        "error_run_failed_title": "Run failed",
        "error_invalid_input_title": "Invalid input",
        "done_title": "Done",
        "done_auto_body": "Auto subtitle completed.\n{path}",
        "done_align_body": "Text alignment completed.\n{path}",
        "error_required_field": "{field} is required.",
        "error_file_not_found": "{field} file not found: {path}",
        "log_auto_started": "[AUTO] started...",
        "log_align_started": "[ALIGN] started...",
        "log_failed": "FAILED: {message}",
    },
    "zh": {
        "window_title": "Audio SRT 工具 - 图形界面",
        "ui_lang_label": "界面语言",
        "common_config": "通用配置",
        "run_log": "运行日志",
        "tab_auto": "自动字幕（音频）",
        "tab_align": "文本对齐",
        "browse": "浏览",
        "run_auto": "运行自动字幕",
        "run_align": "运行文本对齐",
        "label_model": "模型",
        "label_asr_language": "识别语言",
        "label_device": "设备",
        "label_compute_type": "计算精度",
        "label_beam_size": "Beam Size",
        "label_start_lag": "起始延后 (s)",
        "label_end_hold": "结束停留 (s)",
        "label_min_gap": "最小间隔 (s)",
        "label_snap_window": "吸附窗口 (s)",
        "label_max_unit_duration": "最大单条时长",
        "label_split_pause_gap": "分割停顿阈值",
        "label_max_split_depth": "最大分割深度",
        "label_max_early_lead": "最大提前量",
        "label_anchor_min_voice": "锚点最小发声",
        "label_onset_lookahead": "起点前瞻",
        "label_tail_end_guard": "尾段保护",
        "label_audio": "音频",
        "label_transcript_text": "文本稿",
        "label_output_srt": "输出 SRT",
        "check_disable_waveform_snap": "关闭波形吸附",
        "check_date_suffix": "输出文件加日期后缀",
        "dialog_select_audio": "选择音频文件",
        "dialog_select_text": "选择文本文件",
        "dialog_select_output_srt": "选择输出 SRT 文件",
        "filetype_audio": "音频文件",
        "filetype_text": "文本文件",
        "filetype_srt": "SRT 文件",
        "filetype_all": "所有文件",
        "warn_running_title": "任务进行中",
        "warn_running_body": "已有任务正在运行，请稍候。",
        "error_run_failed_title": "运行失败",
        "error_invalid_input_title": "输入无效",
        "done_title": "完成",
        "done_auto_body": "自动字幕已完成。\n{path}",
        "done_align_body": "文本对齐已完成。\n{path}",
        "error_required_field": "{field} 不能为空。",
        "error_file_not_found": "{field} 文件不存在：{path}",
        "log_auto_started": "[AUTO] 开始...",
        "log_align_started": "[ALIGN] 开始...",
        "log_failed": "FAILED: {message}",
    },
}

UI_LANGUAGE_CHOICES = (
    ("zh", "中文"),
    ("en", "English"),
)

UI_LANGUAGE_CODE_TO_LABEL = dict(UI_LANGUAGE_CHOICES)
UI_LANGUAGE_LABEL_TO_CODE = {label: code for code, label in UI_LANGUAGE_CHOICES}


class SubtitleGuiApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("980x760")
        self.minsize(920, 680)

        self._worker: Optional[threading.Thread] = None
        self._build_vars()
        self._build_ui()
        self._apply_ui_language()

    def _build_vars(self) -> None:
        self.ui_language_code_var = tk.StringVar(value="zh")
        self.ui_language_display_var = tk.StringVar(
            value=UI_LANGUAGE_CODE_TO_LABEL.get(self.ui_language_code_var.get(), "中文")
        )

        self.model_var = tk.StringVar(value="small")
        self.language_var = tk.StringVar(value="zh")
        self.device_var = tk.StringVar(value="auto")
        self.compute_type_var = tk.StringVar(value="int8")
        self.beam_size_var = tk.StringVar(value="5")

        self.start_lag_var = tk.StringVar(value="0.03")
        self.end_hold_var = tk.StringVar(value="0.12")
        self.min_gap_var = tk.StringVar(value="0.03")
        self.snap_window_var = tk.StringVar(value="0.30")
        self.max_unit_duration_var = tk.StringVar(value="5.80")
        self.split_pause_gap_var = tk.StringVar(value="0.55")
        self.max_split_depth_var = tk.StringVar(value="2")
        self.max_early_lead_var = tk.StringVar(value="0.04")
        self.anchor_min_voice_var = tk.StringVar(value="0.28")
        self.onset_lookahead_var = tk.StringVar(value="1.20")
        self.tail_end_guard_var = tk.StringVar(value="0.08")

        self.no_waveform_snap_var = tk.BooleanVar(value=False)
        self.date_suffix_var = tk.BooleanVar(value=True)

        self.auto_audio_var = tk.StringVar(value="")
        self.auto_output_var = tk.StringVar(value="")

        self.align_audio_var = tk.StringVar(value="")
        self.align_text_var = tk.StringVar(value="")
        self.align_output_var = tk.StringVar(value="")

    def _t(self, key: str, **kwargs: object) -> str:
        lang = self.ui_language_code_var.get()
        catalog = UI_TEXTS.get(lang, UI_TEXTS["en"])
        template = catalog.get(key, UI_TEXTS["en"].get(key, key))
        return template.format(**kwargs) if kwargs else template

    def _sync_ui_language_display(self) -> None:
        code = self.ui_language_code_var.get()
        display = UI_LANGUAGE_CODE_TO_LABEL.get(code, UI_LANGUAGE_CODE_TO_LABEL["zh"])
        self.ui_language_display_var.set(display)

    def _on_ui_language_selected(self, _event: object = None) -> None:
        selected = self.ui_language_display_var.get()
        code = UI_LANGUAGE_LABEL_TO_CODE.get(selected, "zh")
        if code == self.ui_language_code_var.get():
            return
        self.ui_language_code_var.set(code)
        self._apply_ui_language()

    def _apply_ui_language(self) -> None:
        self._sync_ui_language_display()
        self.title(self._t("window_title"))

        self.ui_language_label.configure(text=self._t("ui_lang_label"))
        self.common_frame.configure(text=self._t("common_config"))
        self.log_frame.configure(text=self._t("run_log"))
        self.notebook.tab(self.auto_tab, text=self._t("tab_auto"))
        self.notebook.tab(self.align_tab, text=self._t("tab_align"))

        for key, label_widget in self._common_label_widgets.items():
            label_widget.configure(text=self._t(key))

        self.no_waveform_snap_check.configure(text=self._t("check_disable_waveform_snap"))
        self.date_suffix_check.configure(text=self._t("check_date_suffix"))

        self.auto_audio_label.configure(text=self._t("label_audio"))
        self.auto_output_label.configure(text=self._t("label_output_srt"))
        self.align_audio_label.configure(text=self._t("label_audio"))
        self.align_text_label.configure(text=self._t("label_transcript_text"))
        self.align_output_label.configure(text=self._t("label_output_srt"))

        self.auto_audio_browse_btn.configure(text=self._t("browse"))
        self.auto_output_browse_btn.configure(text=self._t("browse"))
        self.align_audio_browse_btn.configure(text=self._t("browse"))
        self.align_text_browse_btn.configure(text=self._t("browse"))
        self.align_output_browse_btn.configure(text=self._t("browse"))

        self.auto_run_btn.configure(text=self._t("run_auto"))
        self.align_run_btn.configure(text=self._t("run_align"))

    def _build_ui(self) -> None:
        top = ttk.Frame(self, padding=12)
        top.pack(fill=tk.BOTH, expand=True)

        language_row = ttk.Frame(top)
        language_row.pack(fill=tk.X, expand=False, pady=(0, 8))
        self.ui_language_label = ttk.Label(language_row)
        self.ui_language_label.pack(side=tk.RIGHT, padx=(0, 8))
        self.ui_language_combo = ttk.Combobox(
            language_row,
            textvariable=self.ui_language_display_var,
            values=[label for _, label in UI_LANGUAGE_CHOICES],
            width=10,
            state="readonly",
        )
        self.ui_language_combo.pack(side=tk.RIGHT)
        self.ui_language_combo.bind("<<ComboboxSelected>>", self._on_ui_language_selected)

        self.common_frame = ttk.LabelFrame(top, padding=10)
        self.common_frame.pack(fill=tk.X, expand=False)
        self._build_common_config(self.common_frame)

        self.notebook = ttk.Notebook(top)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.auto_tab = ttk.Frame(self.notebook, padding=10)
        self.align_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.auto_tab, text="")
        self.notebook.add(self.align_tab, text="")

        self._build_auto_tab(self.auto_tab)
        self._build_align_tab(self.align_tab)

        self.log_frame = ttk.LabelFrame(top, padding=8)
        self.log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.log_text = tk.Text(self.log_frame, height=14, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.configure(state=tk.DISABLED)

    def _build_common_config(self, parent: ttk.LabelFrame) -> None:
        rows = [
            ("label_model", self.model_var),
            ("label_asr_language", self.language_var),
            ("label_device", self.device_var),
            ("label_compute_type", self.compute_type_var),
            ("label_beam_size", self.beam_size_var),
            ("label_start_lag", self.start_lag_var),
            ("label_end_hold", self.end_hold_var),
            ("label_min_gap", self.min_gap_var),
            ("label_snap_window", self.snap_window_var),
            ("label_max_unit_duration", self.max_unit_duration_var),
            ("label_split_pause_gap", self.split_pause_gap_var),
            ("label_max_split_depth", self.max_split_depth_var),
            ("label_max_early_lead", self.max_early_lead_var),
            ("label_anchor_min_voice", self.anchor_min_voice_var),
            ("label_onset_lookahead", self.onset_lookahead_var),
            ("label_tail_end_guard", self.tail_end_guard_var),
        ]

        self._common_label_widgets: dict[str, ttk.Label] = {}
        for idx, (label_key, var) in enumerate(rows):
            row = idx // 4
            col = (idx % 4) * 2
            label_widget = ttk.Label(parent)
            label_widget.grid(row=row, column=col, sticky=tk.W, padx=(0, 6), pady=3)
            ttk.Entry(parent, textvariable=var, width=14).grid(
                row=row, column=col + 1, sticky=tk.W, padx=(0, 12), pady=3
            )
            self._common_label_widgets[label_key] = label_widget

        chk_row = (len(rows) + 3) // 4
        self.no_waveform_snap_check = ttk.Checkbutton(
            parent,
            variable=self.no_waveform_snap_var,
        )
        self.no_waveform_snap_check.grid(row=chk_row, column=0, columnspan=2, sticky=tk.W, pady=(8, 0))
        self.date_suffix_check = ttk.Checkbutton(
            parent,
            variable=self.date_suffix_var,
        )
        self.date_suffix_check.grid(row=chk_row, column=2, columnspan=2, sticky=tk.W, pady=(8, 0))

    def _build_auto_tab(self, parent: ttk.Frame) -> None:
        self.auto_audio_label, self.auto_audio_browse_btn = self._path_row(
            parent, 0, self.auto_audio_var, self._browse_audio
        )
        self.auto_output_label, self.auto_output_browse_btn = self._path_row(
            parent, 1, self.auto_output_var, self._browse_srt_output
        )

        self.auto_run_btn = ttk.Button(parent, command=self._run_auto)
        self.auto_run_btn.grid(row=2, column=1, sticky=tk.W, pady=(10, 0))

    def _build_align_tab(self, parent: ttk.Frame) -> None:
        self.align_audio_label, self.align_audio_browse_btn = self._path_row(
            parent, 0, self.align_audio_var, self._browse_audio
        )
        self.align_text_label, self.align_text_browse_btn = self._path_row(
            parent, 1, self.align_text_var, self._browse_text
        )
        self.align_output_label, self.align_output_browse_btn = self._path_row(
            parent, 2, self.align_output_var, self._browse_srt_output
        )

        self.align_run_btn = ttk.Button(parent, command=self._run_alignment)
        self.align_run_btn.grid(row=3, column=1, sticky=tk.W, pady=(10, 0))

    def _path_row(
        self,
        parent: ttk.Frame,
        row: int,
        variable: tk.StringVar,
        browse_callback: Callable[[tk.StringVar], None],
    ) -> tuple[ttk.Label, ttk.Button]:
        label_widget = ttk.Label(parent)
        label_widget.grid(row=row, column=0, sticky=tk.W, pady=4, padx=(0, 8))
        ttk.Entry(parent, textvariable=variable, width=82).grid(row=row, column=1, sticky=tk.W, pady=4)
        browse_btn = ttk.Button(
            parent,
            command=lambda var=variable, cb=browse_callback: cb(var),
        )
        browse_btn.grid(row=row, column=2, sticky=tk.W, padx=(8, 0), pady=4)
        return label_widget, browse_btn

    def _browse_audio(self, target_var: tk.StringVar) -> None:
        path = filedialog.askopenfilename(
            title=self._t("dialog_select_audio"),
            filetypes=[
                (self._t("filetype_audio"), "*.wav *.mp3 *.m4a *.aac *.flac *.ogg"),
                (self._t("filetype_all"), "*.*"),
            ],
        )
        if path:
            target_var.set(path)

    def _browse_text(self, target_var: tk.StringVar) -> None:
        path = filedialog.askopenfilename(
            title=self._t("dialog_select_text"),
            filetypes=[(self._t("filetype_text"), "*.txt"), (self._t("filetype_all"), "*.*")],
        )
        if path:
            target_var.set(path)

    def _browse_srt_output(self, target_var: tk.StringVar) -> None:
        path = filedialog.asksaveasfilename(
            title=self._t("dialog_select_output_srt"),
            defaultextension=".srt",
            filetypes=[(self._t("filetype_srt"), "*.srt"), (self._t("filetype_all"), "*.*")],
        )
        if path:
            target_var.set(path)

    def _append_log(self, message: str) -> None:
        stamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{stamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _set_busy(self, busy: bool) -> None:
        cursor = "watch" if busy else ""
        self.configure(cursor=cursor)

    def _make_worker_logger(self, prefix: str) -> Callable[[str], None]:
        def emit(message: str) -> None:
            self.after(0, lambda m=message: self._append_log(f"{prefix} {m}"))

        return emit

    def _build_config(self) -> AlignmentConfig:
        language = self.language_var.get().strip() or None
        args = Namespace(
            model=self.model_var.get().strip() or "small",
            device=self.device_var.get().strip() or "auto",
            compute_type=self.compute_type_var.get().strip() or "int8",
            language=language,
            beam_size=int(self.beam_size_var.get()),
            start_lag=float(self.start_lag_var.get()),
            end_hold=float(self.end_hold_var.get()),
            min_gap=float(self.min_gap_var.get()),
            snap_window=float(self.snap_window_var.get()),
            no_waveform_snap=bool(self.no_waveform_snap_var.get()),
            max_unit_duration=float(self.max_unit_duration_var.get()),
            split_pause_gap=float(self.split_pause_gap_var.get()),
            max_split_depth=int(self.max_split_depth_var.get()),
            max_early_lead=float(self.max_early_lead_var.get()),
            anchor_min_voice=float(self.anchor_min_voice_var.get()),
            onset_lookahead=float(self.onset_lookahead_var.get()),
            tail_end_guard=float(self.tail_end_guard_var.get()),
        )
        return build_alignment_config(args)

    def _resolve_output(
        self,
        audio_path: Path,
        output_input: str,
    ) -> Path:
        output_arg = output_input.strip() or None
        out = resolve_output_path(
            audio_path=audio_path,
            output_arg=output_arg,
            with_date_suffix=bool(self.date_suffix_var.get()),
        )
        out.parent.mkdir(parents=True, exist_ok=True)
        return out

    def _require_file(self, raw_path: str, label: str) -> Path:
        value = raw_path.strip()
        if not value:
            raise ValueError(self._t("error_required_field", field=label))
        path = Path(value).expanduser().resolve()
        if not path.exists() or not path.is_file():
            raise ValueError(self._t("error_file_not_found", field=label, path=path))
        return path

    def _run_worker(
        self,
        work_fn: Callable[[], object],
        on_success: Callable[[object], None],
    ) -> None:
        if self._worker is not None and self._worker.is_alive():
            messagebox.showwarning(self._t("warn_running_title"), self._t("warn_running_body"))
            return

        self._set_busy(True)

        def task() -> None:
            try:
                result = work_fn()
            except (Exception, SystemExit) as exc:
                detail = f"{exc}\n{traceback.format_exc(limit=4)}"
                self.after(0, lambda: self._on_worker_error(detail))
                return
            self.after(0, lambda: on_success(result))

        self._worker = threading.Thread(target=task, daemon=True)
        self._worker.start()

    def _on_worker_error(self, detail: str) -> None:
        self._set_busy(False)
        self._append_log(self._t("log_failed", message=detail.splitlines()[0]))
        messagebox.showerror(self._t("error_run_failed_title"), detail)

    def _run_auto(self) -> None:
        try:
            config = self._build_config()
            audio_path = self._require_file(self.auto_audio_var.get(), self._t("label_audio"))
            output_path = self._resolve_output(audio_path, self.auto_output_var.get())
        except Exception as exc:
            messagebox.showerror(self._t("error_invalid_input_title"), str(exc))
            return

        self._append_log(f"[AUTO] audio={audio_path}")
        self._append_log(f"[AUTO] output={output_path}")
        self._append_log(self._t("log_auto_started"))
        worker_log = self._make_worker_logger("[AUTO]")

        def work() -> AutoSubtitleRunResult:
            return run_auto_subtitle_pipeline(
                audio_path=audio_path,
                output_path=output_path,
                config=config,
                progress=worker_log,
            )

        def success(result: object) -> None:
            self._set_busy(False)
            assert isinstance(result, AutoSubtitleRunResult)
            self._append_log(
                "[AUTO] done: "
                f"{result.output_path} | lang={result.detected_language} | "
                f"segments={result.raw_segment_count} | "
                f"entries(raw->refined)={result.raw_entry_count}->{result.refined_entry_count} | "
                f"wave={result.waveform_interval_count}"
            )
            messagebox.showinfo(self._t("done_title"), self._t("done_auto_body", path=result.output_path))

        self._run_worker(work_fn=work, on_success=success)

    def _run_alignment(self) -> None:
        try:
            config = self._build_config()
            audio_path = self._require_file(self.align_audio_var.get(), self._t("label_audio"))
            text_path = self._require_file(self.align_text_var.get(), self._t("label_transcript_text"))
            output_path = self._resolve_output(audio_path, self.align_output_var.get())
        except Exception as exc:
            messagebox.showerror(self._t("error_invalid_input_title"), str(exc))
            return

        self._append_log(f"[ALIGN] audio={audio_path}")
        self._append_log(f"[ALIGN] text={text_path}")
        self._append_log(f"[ALIGN] output={output_path}")
        self._append_log(self._t("log_align_started"))
        worker_log = self._make_worker_logger("[ALIGN]")

        def work() -> object:
            return run_alignment_pipeline(
                audio_path=audio_path,
                text_path=text_path,
                output_path=output_path,
                config=config,
                progress=worker_log,
            )

        def success(result: object) -> None:
            self._set_busy(False)
            self._append_log(
                "[ALIGN] done: "
                f"{result.output_path} | lang={result.detected_language} | "
                f"coverage={result.coverage:.1f}% | "
                f"units={result.raw_unit_count}->{result.refined_unit_count} | "
                f"entries={result.srt_entry_count}"
            )
            messagebox.showinfo(self._t("done_title"), self._t("done_align_body", path=result.output_path))

        self._run_worker(work_fn=work, on_success=success)


def main() -> None:
    # Prevent multiprocessing child workers in frozen app from re-launching GUI.
    mp.freeze_support()
    app = SubtitleGuiApp()
    app.mainloop()


if __name__ == "__main__":
    main()
