# calibre-catalog-read

Calibreの検索・書誌確認と、1冊の本文解析を行う読み取り専用スキルです。解析後もcomments/tagsを自動更新しません。保存したい場合は、生成したJSONL提案をcalibre-metadata-applyへ渡します。

## 必要な環境

- カタログ参照: Node.js >=20、calibredb。
- 本文解析: 追加でPython >=3.11、ebook-convert。PDFの変換失敗時はpdftotextが任意のフォールバック。
- 既存Content server、または既存のローカルライブラリ。サーバーは起動・再設定しません。
- 認証がある場合のみ、既存のCALIBRE_USERNAME/CALIBRE_PASSWORDなどの環境変数。

以下のSKILL_DIRは、インストール先の絶対パスに置き換えます。作業ディレクトリに依存しません。

    SKILL_DIR=/absolute/path/to/calibre-catalog-read
    node "$SKILL_DIR/scripts/calibredb_read.mjs" --help
    node "$SKILL_DIR/scripts/calibredb_read.mjs" libraries --with-library "http://HOST:8080/"
    node "$SKILL_DIR/scripts/calibredb_read.mjs" list --with-library "http://HOST:8080/#LIBRARY_ID" --limit 50
    node "$SKILL_DIR/scripts/calibredb_read.mjs" search --query 'series:"中公文庫"'
    node "$SKILL_DIR/scripts/calibredb_read.mjs" id --book-id 3

最後の2例は接続先を環境変数/configへ設定した場合です。list/searchは既定100件、最大10000件に制限します。possibly_truncated=trueは「全件取得と断定できない」の意味です。該当なしと接続失敗を区別します。idは完全一致だけを返します。

## 接続設定

優先順位:

1. --with-library
2. CALIBRE_WITH_LIBRARY / CALIBRE_LIBRARY_URL / CALIBRE_CONTENT_SERVER_URL
3. ~/.config/calibre-catalog-read/config.json のwith_library

configは--configまたはCALIBRE_CATALOG_CONFIGで切り替えられます。許可するキーはwith_library、library_id、username、password_env、reading_scriptです。reading_scriptは従来の人間向け設定を保持するだけで、コードとして実行しません。

    {"with_library":"http://HOST:8080/#LIBRARY_ID","username":"USER","password_env":"CALIBRE_PASSWORD"}

URLにライブラリがない場合は、--library-id / CALIBRE_LIBRARY_ID / config.library_idが必要です。ブラウザー用の#library_id=...ではなくCLI用#LIBRARY_IDを使います。ライブラリID不明時は、指定サーバーだけをlibrariesで照会できます。

パスワードは--password-envで指定した変数から読み、Calibreの公式ファイル入力形式で一時的に渡します。一時ファイルは0600、作成先ディレクトリは私有、通常終了/エラー時に回収します。値はargvや診断ログに出しません。異常終了時は私有一時ディレクトリが残る場合があります。平文保存機能・暗黙の.env読込・DNS/WSL/Dockerのホスト探索はありません。非SSL時の認証はCalibre側のDigestに任せ、auth-mode等を追加しません。

## 実行可能な解析フロー

### 1. 原本を書き出して準備

    python3 "$SKILL_DIR/scripts/run_analysis_pipeline.py" prepare \
      --book-id 3 --run-id book3-unique-run --lang ja --format EPUB

接続オプションはカタログと同じです。--cache-dirで保存先、--chunk-charsで分割サイズを指定できます。prepare_subagent_input.mjsも同じ準備コマンドの入口です。

status=preparedなら、prepared_inputとinput_sha256が返ります。元ファイル・抽出本文・全パートのSHA256、文字数、書籍UUID、接続先、言語、run IDを保存します。exportには--dont-update-metadataを付け、書き出す原本の内容を変えません。

status=skippedなら解析を開始しません。コミック系のタグはexcluded_content、短い抽出はlow_text_requires_confirmationです。続行の明示確認後だけ、別のrun IDと--force-low-textで再準備できます。空の抽出は続行不可です。画像中心の本を読めたことにする定型文の代替要約はありません。

### 2. 登録と解析

    node "$SKILL_DIR/scripts/run_state.mjs" upsert \
      --run-id book3-unique-run --input-json /absolute/run/subagent_input.json

[解析プロンプト](references/subagent-analysis.prompt.md)、[入力スキーマ](references/subagent-input.schema.json)、[出力スキーマ](references/subagent-analysis.schema.json)を使います。特定の専用agent、モデル、2ターン制、完了方式を固定しません。現在利用できる実行基盤の仕様に従います。

パート単位で実際に読んだIDを返し、そのID・ハッシュ・件数・文字数を照合します。これは自己申告の整合性検証であり、モデルの理解や全文読了を数学的に証明するものではありません。途中までなら必ずpartialです。

### 3. オフライン検証と提案

    node "$SKILL_DIR/scripts/handle_completion.mjs" \
      --run-id book3-unique-run --analysis-json /absolute/analysis.json \
      --proposal-jsonl /absolute/NEW-proposal.jsonl

完了時に再取得・再変換・Calibre書込はしません。登録時から入力が変わった場合、書籍・言語・原本が一致しない場合、欠落/改変パート、不正な範囲申告を拒否します。成功時だけproposal_createdを返します。提案はid、expected_library、expected_uuid、analysisを持ち、更新先の取り違えを防ぎます。

非同期登録を使わない手動実行では、次の明示的なオフライン処理も可能です。

    python3 "$SKILL_DIR/scripts/run_analysis_pipeline.py" complete \
      --prepared-input /absolute/run/subagent_input.json \
      --expected-input-sha256 sha256:PREPARATION_OUTPUT_HASH \
      --analysis-json /absolute/analysis.json --proposal-jsonl /absolute/NEW-proposal.jsonl

## 状態・互換性

- 状態: CALIBRE_CATALOG_STATE_DIR、XDG_STATE_HOME/calibre-catalog-read、~/.local/state/calibre-catalog-readの順。
- キャッシュ: CALIBRE_CATALOG_CACHE_DIR、XDG_CACHE_HOME/calibre-catalog-read、~/.cache/calibre-catalog-readの順。
- 新規runディレクトリ・提案は上書きしません。run状態は排他ロックとatomic rename。完了済みIDを記録して重複を抑止し、失敗状態は自動再実行しません。
- ロック残存時は稼働processと提案生成の有無を調べてから復旧します。自動で古いロックを消しません。
- 旧skill/stateと旧runs.json/SQLiteはそのまま保持します。旧処理は新しい状態ファイルとrun IDで再準備してください。破壊的な自動移行はありません。
- analysis_db.pyは任意のローカル索引です。新DBはlibrary/book/format/hash/langで分離し、旧スキーマは上書きせず拒否します。全文、部分解析、言語、対象の証拠はmanifestが正であり、キャッシュ一致で作業を省略しません。
- エクスポートされた書籍や解析結果は私有データです。公開・自動削除・パッケージへの同梱をしません。

## 検証

スキル単体のhermeticテスト(本番接続なし):

    python3 -m unittest discover -s "$SKILL_DIR/tests" -v

リポジトリ直下では、合成データだけを使う実Calibre連携テストも実行できます。サーバー起動や本番DB書込はありません。

    CALIBRE_NATIVE_TESTS=1 python3 -m unittest discover -s tests -p test_calibre_integration.py -v

仕様確認: [公式calibredbマニュアル](https://manual.calibre-ebook.com/generated/en/calibredb.html)。調査時の公式表示9.16.0、実機CLI検証9.2.1。旧バージョンで未知のオプションが出たら、黙って省略せずhelpと互換性を確認してください。
