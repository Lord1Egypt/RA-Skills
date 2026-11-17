# calibre-metadata-apply

Calibreメタデータを「変更計画の保存 -> 対象/現在値の再確認 -> 適用 -> 再読込検証」で更新します。dry-runが既定です。解析workerから返っただけでは書き込みません。

## クイックスタート

Node.js >=20とcalibredbが必要です。SKILL_DIRをインストール先の絶対パスに置き換えてください。

    SKILL_DIR=/absolute/path/to/calibre-metadata-apply
    node "$SKILL_DIR/scripts/calibredb_apply.mjs" --help
    node "$SKILL_DIR/scripts/calibredb_apply.mjs" \
      --with-library "http://HOST:8080/#LIBRARY_ID" \
      --plan-file /absolute/NEW-plan.json < /absolute/changes.jsonl

内容を確認・承認した同じ計画だけを適用します。計画のdigestは誤編集検出用で、人の承認そのものではありません。

    node "$SKILL_DIR/scripts/calibredb_apply.mjs" \
      --apply --plan-file /absolute/plan.json < /dev/null

applyは新しいJSONL入力を受け付けません。接続先省略時は保存計画の接続先を固定して使います。入力された接続先が計画と違えば拒否します。

## 入力と変更の意味

1行1冊のJSONLです。[例](references/changes.example.md)のコードブロック内の行だけを変更ファイルへコピーしてください。Markdown自体を入力に使わないでください。IDはダミーで、実行承認済みではありません。

- 直接指定: title、title_sort、authors、author_sort、series、series_index、tags、publisher、pubdate、languages、comments。
- 補助指定: analysis、comments_html、analysis_tags、tags_merge、tags_remove。
- カタログからの提案はexpected_library/expected_uuidも保持します。別ライブラリ/別書籍への取り違えを拒否します。
- 未指定は変更しません。title/authorsは必須値なので空不可。任意文字列はnull/空文字で消去。pubdateもnull/空文字で消去可能。series_indexはnull不可、非負の有限数でseriesが必要です。
- authorsは配列推奨。著者名のカンマは保持します。名前中のリテラル&や|はCalibreの--fieldで安全に表せないため、変更前に拒否します。黙って別の著者に分割しません。書誌OPFの個々の著者要素で検証し、表示文字列だけで人数を推定しません。
- pubdateはYYYY-MM-DD。CLIにはUTC時刻を明示し、ホストの時差による前日ずれを防ぎます。
- languagesは実行時ICUが認識するISO639コード。ja/jpn、en/eng等は同じ言語として比較します。未知コードや地域付きタグを黙って削除しません。
- tagsは既定でmerge。tags:[]だけでは消しません。置換/全消去はtags_merge:false、部分削除はtags_removeを使います。
- commentsはコメント全体の置換です。analysisは値をHTML escapeしてOC_ANALYSISマーカー1区画を更新し、既存のその他コメントとタグを保持します。comments_htmlは承認済みraw HTML用です。3方式の同時指定や壊れたマーカーは拒否します。
- analysis.coverageがあればfull/partialとパート数もコメントに残します。元の部分解析を全文解析に見せません。
- タイトル・著者変更でsortが自動追随するとは仮定しません。日本語の読みはworkspaceの設定と根拠を使い、sort自体も変更内容として示します。

## 安全モデルと限界

入力全件を検証し、ID/UUID・表示差分・関連する現在メタデータ・CLI intentを計画に保存します。apply前に全行を照合し、各書込の直前にも再照合します。別のクライアントがタイトル等を変更していた場合も古い計画を拒否します。

set_metadataの成功後は再読込で要求値を検証します。起動失敗・signal・timeout・出力過大を成功扱いしません。失敗/不明な結果が出たら後続行を止め、実際の適用済み行・未実行行を分けます。

stateのattempts/には、書込前にfsyncしたintent、各行のresult、最終集計をJSONLで残します。同じplan digestは1度だけ試行し、ライブラリ単位のローカルロックで同じwrapper同士の競合を抑えます。失敗後はreceiptと現在値を照合して新しい計画を作ります。自動retry/rollbackはありません。

Calibre CLIにはサーバー側の比較交換(CAS)や複数冊の一括transactionがありません。他クライアントとの最終read/write間の競合までは防げません。processが突然終了した場合、ロック/intentが残ります。稼働状態と実値を確認するまでロックやreceiptを消さないでください。別state-dirでロックを迂回しないでください。

## 接続と認証

接続先の優先順位は--with-library、CALIBRE_WITH_LIBRARY / CALIBRE_LIBRARY_URL / CALIBRE_CONTENT_SERVER_URL、config.with_libraryです。URLに#LIBRARY_IDがなければ--library-id / CALIBRE_LIBRARY_ID / config.library_idで補います。ローカル接続は既存metadata.dbを含むディレクトリだけです。

configは~/.config/calibre-metadata-apply/config.json、または--config。許可するキーはwith_library、library_id、username、password_env、state_dir、reading_scriptです。reading_scriptは既存の人間向け並び替え設定として保持し、実行しません。未知キー・未知オプションはエラーです。

パスワードは既存環境変数から取得し、--password-envで変数名を変更できます。Calibreの公式<stdin>入力で渡し、argvや診断、計画には値を入れません。CLIが非対話入力の警告を出す場合も、実際の終了値と結果を検証します。暗黙の.env読込、平文認証保存、DNS/WSL/Docker探索、別ホストへのfailoverはありません。calibre-serverも起動しません。

## 状態と互換性

保存先: --state-dir -> CALIBRE_METADATA_APPLY_STATE_DIR -> config.state_dir -> XDG_STATE_HOME/calibre-metadata-apply -> ~/.local/state/calibre-metadata-apply。計画ファイルは--plan-fileでも指定でき、既存ファイルは上書きしません。

旧skill/state、旧計画、旧認証保存は自動移行/上書きしません。新しい計画を作り直します。--save-auth、--save-plain-password、--server-hosts、auth-mode/auth-schemeは廃止しました。既存reading_script設定は互換性のため受け付けます。

任意の提案作成ジョブ管理:

    node "$SKILL_DIR/scripts/run_state.mjs" upsert --run-id JOB --session-key HANDLE --task "metadata proposal"
    node "$SKILL_DIR/scripts/handle_completion.mjs" --run-id JOB --result-json /absolute/result.json

result.jsonは少なくとも次の形で、run_idが一致する必要があります。

    {"run_id":"JOB","ok":true,"status":"proposal_ready","proposal_file":"/absolute/changes.jsonl"}

完了helperはローカル結果だけを扱い、metadataを書きません。失敗状態は保持し、完了済みIDの再登録を拒否します。特定のagent名や固定の2ターン処理を要求しません。

## テスト

スキル単体のfake CLI/排他・破損・誤適用防止テスト:

    node --test "$SKILL_DIR"/tests/*.test.mjs

リポジトリ直下で、完全に隔離した合成ライブラリを使う実Calibre連携テスト:

    CALIBRE_NATIVE_TESTS=1 python3 -m unittest discover -s tests -p test_calibre_integration.py -v

[公式calibredbマニュアル](https://manual.calibre-ebook.com/generated/en/calibredb.html)と実機9.2.1のhelp/出力を基準に検証しています。本番Content serverへの書込試験は含めません。
