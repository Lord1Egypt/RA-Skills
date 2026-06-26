#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const reportLib = require('./generate-report.js');

const WORKSPACE = reportLib.WORKSPACE;
const REPORTS_DIR = path.join(WORKSPACE, 'reports', 'weekly');
const FRONT_COVER_TEMPLATE_PATH = path.join(REPORTS_DIR, 'assets', 'front-cover-template.pdf');
const ANCHOR_DATE = (process.env.WEEKLY_REPORT_DATE || reportLib.getWibDateKey(new Date())).trim();
const INTERNSHIP_WEEK_ONE_START = (process.env.WEEKLY_REPORT_WEEK_ONE_START || ANCHOR_DATE).trim();
const REPORT_AUTHOR = (process.env.WEEKLY_REPORT_AUTHOR || 'Internship Student').trim();
const REPORT_SCOPE = 'internship';

fs.mkdirSync(REPORTS_DIR, { recursive: true });

main();

function main() {
  const range = getPreviousWeekRange(ANCHOR_DATE);
  const artifacts = reportLib.collectArtifacts({
    targetDates: range.dateKeys,
    scope: REPORT_SCOPE,
  });
  const repoGroups = reportLib.buildRepoGroups(artifacts);
  const themeContext = buildThemeContext(repoGroups);
  const summary = buildSummary(themeContext);
  const narrative = buildNarrative(themeContext);

  const baseName = `weekly-report-${range.startDate}_to_${range.endDate}`;
  const texPath = path.join(REPORTS_DIR, `${baseName}.tex`);
  const jsonPath = path.join(REPORTS_DIR, `${baseName}.json`);
  const pdfPath = path.join(REPORTS_DIR, `${baseName}.pdf`);
  const reportWeekNumber = getInternshipWeekNumber(range.startDate);
  const existingReport = loadExistingWeeklyReportArtifacts({
    texPath,
    jsonPath,
    pdfPath,
  });

  const compileResult = existingReport
    ? {
        ok: true,
        pdfPath,
        texPath,
        note: 'Menggunakan laporan mingguan yang sudah ada tanpa meregenerasi isi laporan.',
      }
    : buildWeeklyReportPdf({
        texPath,
        range,
        summary,
        narrative,
      });
  const frontCoverResult = compileResult.ok
    ? buildFrontCover({
        baseName,
        reportWeekNumber,
      })
    : {
        ok: false,
        pdfPath: null,
        texPath: null,
        note: 'Front cover belum dibuat karena PDF utama belum berhasil dikompilasi.',
      };
  const mergedPdfPath = path.join(REPORTS_DIR, `${baseName}-with-cover.pdf`);
  const mergeResult = compileResult.ok && frontCoverResult.ok
    ? mergePdfFiles({
        outputPath: mergedPdfPath,
        inputPaths: [frontCoverResult.pdfPath, pdfPath],
      })
    : {
        ok: false,
        pdfPath: compileResult.ok ? pdfPath : null,
        note: frontCoverResult.ok
          ? compileResult.note
          : `${compileResult.note} ${frontCoverResult.note}`.trim(),
      };
  const metadata = {
    title: `Laporan Mingguan Kerja Praktek (${range.startLabel} - ${range.endLabel})`,
    anchorDate: ANCHOR_DATE,
    startDate: range.startDate,
    endDate: range.endDate,
    startLabel: range.startLabel,
    endLabel: range.endLabel,
    reportWeekNumber,
    dateKeys: range.dateKeys,
    texPath,
    jsonPath,
    pdfPath: mergeResult.pdfPath,
    bodyPdfPath: compileResult.ok ? pdfPath : null,
    frontCoverPdfPath: frontCoverResult.ok ? frontCoverResult.pdfPath : null,
    summary: existingReport?.summary || summary,
    narrative: existingReport?.narrative || narrative,
    sections: existingReport?.sections,
    repoNames: themeContext.repoNames,
    themes: themeContext.themes,
    note: mergeResult.note,
  };

  fs.writeFileSync(jsonPath, JSON.stringify(metadata, null, 2), 'utf8');
  process.stdout.write(JSON.stringify(metadata, null, 2));
}

function getPreviousWeekRange(anchorDateKey) {
  const anchor = parseDateKey(anchorDateKey);
  const dayOfWeek = anchor.getUTCDay();
  const mondayOffset = (dayOfWeek + 6) % 7;
  const currentWeekMonday = addDays(anchor, -mondayOffset);
  const previousWeekMonday = addDays(currentWeekMonday, -7);
  const previousWeekSunday = addDays(previousWeekMonday, 6);
  const dateKeys = [];

  for (let cursor = previousWeekMonday; cursor <= previousWeekSunday; cursor = addDays(cursor, 1)) {
    dateKeys.push(toDateKey(cursor));
  }

  return {
    anchorDate: anchorDateKey,
    startDate: toDateKey(previousWeekMonday),
    endDate: toDateKey(previousWeekSunday),
    startLabel: reportLib.formatIndonesianDate(toDateKey(previousWeekMonday)),
    endLabel: reportLib.formatIndonesianDate(toDateKey(previousWeekSunday)),
    dateKeys,
  };
}

function buildThemeContext(repoGroups) {
  const themes = reportLib.unique(
    reportLib
      .selectActivityThemes(repoGroups)
      .map((theme) => String(theme || '').trim())
      .filter(Boolean),
  );

  return {
    repoNames: reportLib.unique(repoGroups.map((group) => group.displayName).filter(Boolean)),
    themes,
    hasReportFlow:
      includesAny(themes, ['generate report', 'unduhan pdf', 'backend publik', 'tautan', 'service generate report']),
    hasAiRequest:
      includesAny(themes, ['openai', 'gpt-5', 'gpt-5.4', 'payload request']),
    hasModelConfig:
      includesAny(themes, ['konfigurasi beberapa agent', 'default model', 'mini dan nano']),
    hasOrchestration:
      includesAny(themes, ['provider extension', 'orkestrasi', 'opsi model tambahan', 'agentorchestration']),
    hasValidation:
      includesAny(themes, ['unit test', 'kompatibel', 'validasi']),
    hasAnyWork: repoGroups.length > 0,
  };
}

function buildSummary(context) {
  if (!context.hasAnyWork) {
    return 'Pada periode ini belum ditemukan aktivitas pengembangan yang relevan untuk dirangkum sebagai laporan kerja praktik.';
  }

  const focusAreas = [];
  if (context.hasReportFlow) {
    focusAreas.push('pembenahan alur pembuatan laporan');
  }
  if (context.hasAiRequest || context.hasModelConfig) {
    focusAreas.push('penyesuaian integrasi layanan AI');
  }
  if (context.hasOrchestration) {
    focusAreas.push('penyempurnaan komponen orkestrasi agent');
  }

  const focusText = focusAreas.length > 0
    ? reportLib.joinHumanList(focusAreas)
    : 'pengembangan dan penyempurnaan sistem backend';

  return `Pada periode ini, kegiatan kerja praktik difokuskan pada ${focusText} agar backend Moncube dan komponen pendukungnya dapat berjalan dengan lebih rapi, konsisten, dan siap digunakan pada lingkungan implementasi yang lebih nyata.`;
}

function buildNarrative(context) {
  if (!context.hasAnyWork) {
    return [
      'Pada periode laporan ini belum terdapat aktivitas pengembangan yang cukup relevan untuk disusun menjadi uraian kerja praktik. Oleh karena itu, laporan ini hanya mencatat bahwa belum ada pekerjaan teknis utama yang dapat dijadikan bahan evaluasi atau dokumentasi mingguan.',
    ];
  }

  const paragraphs = [
    'Pada periode ini, kegiatan kerja praktik dipusatkan pada pengembangan backend Moncube serta penyempurnaan komponen pendukung integrasi layanan kecerdasan buatan. Pekerjaan yang dilakukan tidak hanya berfokus pada penambahan dukungan fitur, tetapi juga pada penyesuaian implementasi yang sudah ada agar dapat digunakan dengan lebih baik, lebih konsisten, dan lebih sesuai dengan kebutuhan sistem secara keseluruhan.',
  ];

  if (context.hasReportFlow) {
    paragraphs.push(
      'Salah satu fokus utama berada pada pembenahan fitur pembuatan laporan. Penyesuaian dilakukan agar file hasil generate dapat diakses melalui alamat backend publik yang sesuai dengan lingkungan implementasi, sehingga alur unduh dan penggunaan hasil laporan menjadi lebih masuk akal bagi pengguna. Perbaikan ini penting karena fitur pelaporan tidak hanya perlu berhasil membuat dokumen, tetapi juga harus memastikan bahwa hasil akhirnya benar-benar dapat dipakai dalam proses kerja sehari-hari.',
    );
  }

  if (context.hasAiRequest || context.hasModelConfig) {
    paragraphs.push(
      'Selain itu, integrasi layanan AI juga disempurnakan melalui penyesuaian mekanisme request ke OpenAI agar penggunaan model GPT-5.4 dapat berjalan dengan parameter yang lebih tepat. Konfigurasi model pada beberapa bagian sistem turut diperbarui supaya pemakaian model menjadi lebih seragam dan sesuai dengan kebutuhan aplikasi. Dengan penyesuaian ini, perilaku sistem diharapkan menjadi lebih stabil ketika fitur berbasis AI dijalankan dalam skenario penggunaan yang sebenarnya.',
    );
  }

  if (context.hasOrchestration) {
    paragraphs.push(
      'Pada komponen pendukung, library orkestrasi agent AI juga ditingkatkan agar mampu meneruskan opsi model tambahan dan mendukung integrasi provider dengan lebih baik. Penyempurnaan ini dilakukan untuk membuat hubungan antar komponen menjadi lebih fleksibel, sekaligus mempermudah pengembangan lanjutan ketika sistem membutuhkan variasi model atau pengaturan layanan yang lebih kompleks.',
    );
  }

  if (context.hasValidation) {
    paragraphs.push(
      'Agar perubahan yang dilakukan tidak berhenti pada sisi implementasi saja, penyesuaian tersebut juga diiringi dengan langkah validasi untuk menjaga kompatibilitas komponen yang terhubung. Dengan demikian, pembaruan yang diterapkan tidak hanya menambah kemampuan sistem, tetapi juga tetap memperhatikan kestabilan dan keberlanjutan proses pengembangan berikutnya.',
    );
  }

  paragraphs.push(
    'Secara keseluruhan, rangkaian pekerjaan pada periode ini memberikan dampak langsung terhadap kualitas fitur pelaporan dan integrasi AI pada sistem backend. Dengan alur generate report yang lebih sesuai, konfigurasi model yang lebih konsisten, serta dukungan orkestrasi yang lebih matang, fondasi sistem menjadi lebih siap untuk digunakan dan dikembangkan lebih lanjut dalam konteks kerja praktik.',
  );

  return paragraphs;
}

function renderLatex({ range, summary, narrative }) {
  const paragraphs = narrative.map((paragraph) => escapeLatex(paragraph)).join('\n\n');

  return String.raw`\documentclass[11pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{parskip}

\title{Laporan Mingguan Kerja Praktek\\${escapeLatex(range.startLabel)} -- ${escapeLatex(range.endLabel)}}
\author{${escapeLatex(REPORT_AUTHOR)}}
\date{Disusun pada ${escapeLatex(reportLib.formatIndonesianDate(ANCHOR_DATE))}}

\begin{document}
\maketitle

\noindent\textbf{Ringkasan Singkat}\\
${escapeLatex(summary)}

\vspace{1em}
\noindent\textbf{Uraian Kegiatan}\\
${paragraphs}

\end{document}
`;
}

function buildFrontCover({ baseName, reportWeekNumber }) {
  if (!fs.existsSync(FRONT_COVER_TEMPLATE_PATH)) {
    return {
      ok: false,
      pdfPath: null,
      texPath: null,
      note: 'Template front cover belum tersedia, sehingga laporan mingguan dikirim tanpa cover tambahan.',
    };
  }

  if (!commandExists('pdflatex')) {
    return {
      ok: false,
      pdfPath: null,
      texPath: null,
      note: 'Template front cover tersedia, tetapi pdflatex belum tersedia untuk membuat cover otomatis.',
    };
  }

  const texPath = path.join(REPORTS_DIR, `${baseName}-cover.tex`);
  const pdfPath = path.join(REPORTS_DIR, `${baseName}-cover.pdf`);
  const weekLabel = reportWeekNumber ? `Minggu ${reportWeekNumber}` : 'Minggu';
  const latex = renderFrontCoverLatex({
    templateRelativePath: 'assets/front-cover-template.pdf',
    weekLabel,
  });

  fs.writeFileSync(texPath, latex, 'utf8');

  const compileResult = compilePdf(texPath);

  return {
    ok: compileResult.ok,
    pdfPath: compileResult.ok ? pdfPath : null,
    texPath,
    note: compileResult.ok
      ? `Front cover berhasil dibuat dengan label ${weekLabel}.`
      : `Sumber front cover berhasil dibuat, tetapi kompilasi cover gagal. ${compileResult.note}`.trim(),
  };
}

function renderFrontCoverLatex({ templateRelativePath, weekLabel }) {
  return String.raw`\documentclass[a4paper]{article}
\usepackage[margin=0cm]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{tikz}
\usepackage{graphicx}
\pagestyle{empty}

\begin{document}
\begin{tikzpicture}[remember picture,overlay]
  \node[anchor=center] at (current page.center) {\includegraphics[width=\paperwidth,height=\paperheight,page=1]{${templateRelativePath}}};
  \fill[white] ([xshift=-1.9cm,yshift=10.45cm]current page.center) rectangle ([xshift=1.9cm,yshift=9.72cm]current page.center);
  \node[font={\sffamily\fontsize{14}{16}\selectfont}, text=black] at ([yshift=10.08cm]current page.center) {${escapeLatex(weekLabel)}};
\end{tikzpicture}
\null
\end{document}
`;
}

function loadExistingWeeklyReportArtifacts({ texPath, jsonPath, pdfPath }) {
  if (!fs.existsSync(texPath) || !fs.existsSync(pdfPath)) {
    return null;
  }

  let metadata = null;

  if (fs.existsSync(jsonPath)) {
    try {
      metadata = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
    } catch {
      metadata = null;
    }
  }

  return {
    summary: metadata?.summary || null,
    narrative: Array.isArray(metadata?.narrative) ? metadata.narrative : null,
    sections: Array.isArray(metadata?.sections) ? metadata.sections : null,
  };
}

function buildWeeklyReportPdf({ texPath, range, summary, narrative }) {
  const latex = renderLatex({
    range,
    summary,
    narrative,
  });

  fs.writeFileSync(texPath, latex, 'utf8');
  return compilePdf(texPath);
}

function compilePdf(texPath) {
  const pdfPath = texPath.replace(/\.tex$/i, '.pdf');
  const basename = path.basename(texPath);
  const cwd = path.dirname(texPath);

  const check = spawnSync('bash', ['-lc', 'command -v pdflatex >/dev/null 2>&1'], {
    encoding: 'utf8',
  });

  if (check.status !== 0) {
    return {
      ok: false,
      note: 'LaTeX source generated, tetapi pdflatex belum tersedia sehingga PDF tidak dapat dibuat otomatis.',
    };
  }

  for (let index = 0; index < 2; index += 1) {
    const result = spawnSync('pdflatex', ['-interaction=nonstopmode', '-halt-on-error', basename], {
      cwd,
      encoding: 'utf8',
    });

    if (result.status !== 0) {
      return {
        ok: false,
        note: 'LaTeX source generated, tetapi proses kompilasi PDF gagal dan perlu dicek manual.',
      };
    }
  }

  return {
    ok: fs.existsSync(pdfPath),
    note: fs.existsSync(pdfPath)
      ? 'PDF berhasil dibuat dari sumber LaTeX.'
      : 'LaTeX source generated, tetapi file PDF belum terbentuk.',
  };
}

function mergePdfFiles({ outputPath, inputPaths }) {
  if (!commandExists('mutool')) {
    return {
      ok: false,
      pdfPath: inputPaths.at(-1) || null,
      note: 'PDF utama berhasil dibuat, tetapi mutool belum tersedia sehingga front cover belum dapat digabungkan otomatis.',
    };
  }

  const result = spawnSync('mutool', ['merge', '-o', outputPath, ...inputPaths], {
    encoding: 'utf8',
  });

  if (result.status !== 0 || !fs.existsSync(outputPath)) {
    return {
      ok: false,
      pdfPath: inputPaths.at(-1) || null,
      note: 'PDF utama berhasil dibuat, tetapi penggabungan front cover ke PDF utama gagal dan perlu dicek manual.',
    };
  }

  return {
    ok: true,
    pdfPath: outputPath,
    note: 'PDF mingguan berhasil dibuat dan front cover berhasil ditambahkan di halaman depan.',
  };
}

function commandExists(command) {
  const result = spawnSync('bash', ['-lc', `command -v ${command} >/dev/null 2>&1`], {
    encoding: 'utf8',
  });
  return result.status === 0;
}

function includesAny(values, keywords) {
  const haystack = values.map((value) => String(value || '').toLowerCase());
  return keywords.some((keyword) => haystack.some((value) => value.includes(String(keyword).toLowerCase())));
}

function parseDateKey(dateKey) {
  const [year, month, day] = String(dateKey).split('-').map(Number);
  return new Date(Date.UTC(year, month - 1, day));
}

function getInternshipWeekNumber(reportStartDateKey) {
  const reportStart = parseDateKey(reportStartDateKey);
  const weekOneStart = parseDateKey(INTERNSHIP_WEEK_ONE_START);
  const diffDays = Math.round((reportStart.getTime() - weekOneStart.getTime()) / 86400000);

  if (diffDays < 0) {
    return null;
  }

  return Math.floor(diffDays / 7) + 1;
}

function addDays(date, days) {
  const clone = new Date(date.getTime());
  clone.setUTCDate(clone.getUTCDate() + days);
  return clone;
}

function toDateKey(date) {
  return date.toISOString().slice(0, 10);
}

function escapeLatex(value) {
  return String(value || '')
    .replace(/\\/g, '\\textbackslash{}')
    .replace(/&/g, '\\&')
    .replace(/%/g, '\\%')
    .replace(/\$/g, '\\$')
    .replace(/#/g, '\\#')
    .replace(/_/g, '\\_')
    .replace(/\{/g, '\\{')
    .replace(/\}/g, '\\}')
    .replace(/~/g, '\\textasciitilde{}')
    .replace(/\^/g, '\\textasciicircum{}');
}
