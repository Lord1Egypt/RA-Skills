# calibre-reference-ingest

調査で参照した**電子書籍ファイルと、それを含む圧縮ファイル**をCalibreへ取り込み、出典URLとタグで整理するスキル。

常設の自動保存指示がある場合は、個別の依頼を待たず処理する。Webクリップは対象外。検索結果全件や未使用の候補を収集せず、重複も再登録しない。成功の定型報告は省き、失敗や判断が必要な場合は知らせる。

## 組み合わせるスキル

このスキルは「新しい本の追加」だけを担当する。次の2つと組み合わせて使う前提で、単体では重複確認や既存タグの修正ができない。

- [calibre-catalog-read](https://clawhub.ai/nextaltair/skills/calibre-catalog-read): 取り込み前の重複確認、似た書名・既存タグ語彙の確認(読み取り専用)。
- [calibre-metadata-apply](https://clawhub.ai/nextaltair/skills/calibre-metadata-apply): 既存の本のタグやメタデータの変更。このスキルは既存の本を書き換えない。

    openclaw skills install @nextaltair/calibre-catalog-read
    openclaw skills install @nextaltair/calibre-metadata-apply

## 対象

- 電子書籍原本: PDF、EPUB/KEPUB、MOBI、AZW/AZW3/AZW4、PRC、FB2、DjVu、CBZ/CBR/CB7。
- 書籍入り圧縮ファイル: ZIP、7z、RAR、TAR、TAR.GZ/BZ2/XZ。中の対象書籍を個別登録する。全対象の保存確認後、取り込み専用に取得した圧縮ファイルや展開物は片付ける。別の原本バックアップは作らない。
- EPUBやCBZ/CBR/CB7自体は書籍。内部の画像・HTMLまで展開して別資料にしない。

**対象外:** Web本文クリップ、HTML/MHTML/HTMLZ、記事のTXT/Markdown、検索結果一覧、生成要約本、ブラウザー印刷PDF。WebページをEPUB/PDFへ変換して保存する抜け道も使わない。出版社などが配布する本物のPDF・EPUBへのリンク取得は対象。

取得日時は記録せず、日付管理はCalibre標準の登録日(timestamp)を利用する。資料自身の公開日・版は判明していれば別途保持する。

## 必要環境

- Python >=3.11、calibredb。確認済み一時コピーの後片付けにはtrash (trash-cli) を使う。
- 圧縮ファイルの処理にはシステムのlibarchive共有ライブラリ。Pythonのctypesから既知のnative形式/フィルターだけを呼ぶ。Python追加パッケージ・外部展開コマンド・変換サービスは不要。
- サーバーや認証はworkspaceのAGENTS.md Toolsから取得。既存ライブラリを--with-libraryまたはCALIBRE_WITH_LIBRARYで指定する。URLは http://HOST:8080/#LIBRARY_ID。
- 認証はCALIBRE_USERNAME/CALIBRE_PASSWORDまたは--username/--password-env。パスワードはcalibredbの標準入力へ渡し、計画・引数へ記録しない。

サーバー起動、ホスト自動探索、別ライブラリの自動作成、DRMや暗号化の解除は行わない。

## 電子書籍の取り込み

SKILL.mdがエージェント向け手順。references/input.example.jsonを参考に書誌情報を作成する。

    python3 scripts/reference_ingest.py prepare --input-json /absolute/reference.json --run-dir /absolute/NEW-run --with-library 'http://HOST:8080/#LIBRARY_ID'
    python3 scripts/reference_ingest.py apply --apply --plan-file /absolute/NEW-run/plan.json
    python3 scripts/reference_ingest.py verify --plan-file /absolute/NEW-run/plan.json
    python3 scripts/reference_ingest.py cleanup --apply --plan-file /absolute/NEW-run/plan.json

prepareは原本コピー・OPF生成・重複検索だけで、Calibreを変更しない。文書の変換はしない。保存計画の技術的確認は必要だが、常設許可のある通常の新規保存でユーザーの再確認は不要。

decision=review_existingは重複/同名候補の確認が必要。既存の同一資料はそのIDを使う。改訂版や別資料との衝突を強制突破しない。既存タグ変更はcalibre-metadata-applyで扱い、他のメタデータを保護する。

## 圧縮ファイル

    python3 scripts/ebook_archive.py list --archive /absolute/books.zip
    python3 scripts/ebook_archive.py extract --archive /absolute/books.zip --sha256 INVENTORY_HASH --member-id 1 --output-dir /absolute/NEW-extraction

listのmembersから参照対象の書籍を選ぶ。member-idを固定値で推測しない。extractが返すfileを通常の入力JSONへ入れ、archive_memberとarchive_sha256も返された値のまま追加する。出典URLは元の圧縮ファイルのURL/配布ページを使う。

同一圧縮ファイル内の複数冊は、URL+メンバー名で識別する。個別の内容SHA256は別経路の同一書籍も検出する。コンテナを空のZIP本として登録したり、配下のWebクリップや入れ子の圧縮ファイルを自動処理したりしない。

安全制約:

- 入力 <=1 GiB、最大2000エントリ、1メンバー <=200 MiB、展開総量 <=512 MiB。SIGALRM対応環境のCLIは120秒で停止する。
- 全エントリを事前点検。リンク・特殊ファイル・暗号化・親ディレクトリ参照・絶対/ドライブパス・名前衝突を拒否する。
- メンバーのパスを出力先として使わない。新しい専用ディレクトリにebook.拡張子として1冊だけ書き出す。
- 元の圧縮ファイルのSHA256を抽出前後で検証。失敗したebook.partialは取り込まない。既存出力への上書き・自動リトライはしない。
- libarchiveの不在、破損、対応外形式は明示的な失敗。対象書籍がない正常結果とは区別する。

## 保存と回復

取り込み中だけ原本・圧縮ファイル・展開物をプライベートなstate/cacheへ置く。保存先はCalibreライブラリとし、その既存バックアップとは別に原本やZIPを保管し続けない。

cleanup --applyは成功receiptと最新メタデータを確認し、Calibreから一時exportしたファイルのSHA256を照合してから、RUN内のstaged ebookをtrashへ移す。--applyなしは読み取り専用preview。小さなextraction.json、metadata.opf、plan.json、apply-receipt.jsonlは照合用に残す。verifyは作業コピーの片付け後も利用できる。

helperはmetadata.fileが指す任意の入力ファイルを削除しない。mainは、このタスク用にダウンロード/展開したことが分かる入力について、全対象の保存成功後にtrashで片付ける。既存のユーザー所有ファイルや共有入力を一括削除する処理ではない。失敗/不明/未完了の対象に必要な一時データだけは解決まで残す。trashの不在や失敗は報告し、永久削除やゴミ箱を空にする代替動作はしない。

計画はschema 2。旧schema 1/Webクリップ計画は拒否し、そのまま保存する。旧クリップファイルを本に変えて再利用しない。

適用済み/失敗receiptがある計画は再適用不可。verifyとcalibre-catalog-readで実データを照合する。メタデータだけ失敗した場合も、新規追加を繰り返さず既存IDの承認済み修復へ進む。Calibre内の本の自動削除・ロールバックはしない。

ロックはXDG_STATE_HOME/calibre-reference-ingest/locks (既定 ~/.local/state/...)。他ホスト/他クライアントまで排他する仕組みではない。プロセスや他作業を確認せずロックを消してはならない。

## 検証と限界

    uv run --no-project --offline python3 -m unittest discover -s calibre-reference-ingest/tests -v
    CALIBRE_NATIVE_TESTS=1 uv run --no-project --offline python3 -m unittest discover -s calibre-reference-ingest/tests -v

後者は隔離した一時ライブラリと合成書籍のみを使う。本番変更やサーバー起動はない。Calibreとlibarchiveが必要。

ヘッダー確認は完全な書籍検証ではない。本文/書誌の正しさや公開権限は別途確認する。apply成功はメタデータと形式の存在の再確認であり、レンダリングや保存バイト列の完全一致を常に保証しない。PDF/EPUBの原本保持、ZIP内2冊の個別登録、7zと圧縮TAR、安全性停止条件はテストする。RARデコーダーはlibarchive依存で、初回に実ファイルの正常展開を確認する。

## 仕様根拠

- https://manual.calibre-ebook.com/generated/en/calibredb.html
- https://manual.calibre-ebook.com/faq.html#what-formats-does-calibre-support-conversion-to-from
- https://github.com/libarchive/libarchive (archive_read / archive_entry API)
- Calibre 9.2.1実体のCLI helpと隔離ライブラリで確認。
